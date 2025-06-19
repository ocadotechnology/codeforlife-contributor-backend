"""
© Ocado Group
Created on 19/06/2025 at 11:30:00(+00:00).
"""

import logging
import typing as t
from datetime import datetime, timedelta

import jwt
import requests
from codeforlife.permissions import BasePermission
from codeforlife.types import JsonDict
from django.conf import settings
from django.utils import timezone
from jwt.algorithms import RSAAlgorithm


class HasGitHubOidcToken(BasePermission):
    """
    Checks the incoming request is being has a GitHub-issued OIDC token.

    https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect
    """

    gh_oidc_issuer = "https://token.actions.githubusercontent.com"
    gh_jwks_url = f"{gh_oidc_issuer}/.well-known/jwks"

    # Cache for JWKS to avoid fetching on every request.
    gh_jwks: t.Optional[t.List[JsonDict]] = None
    gh_jwks_last_fetched: t.Optional[datetime] = None
    JWKS_CACHE_TTL = 3600

    def _get_github_jwks(self):
        """Fetches GitHub's JWKS (JSON Web Key Set) and caches it."""
        now = timezone.now()

        if (
            self.gh_jwks
            and self.gh_jwks_last_fetched
            and (now - self.gh_jwks_last_fetched)
            >= timedelta(seconds=self.JWKS_CACHE_TTL)
        ):
            return self.gh_jwks

        response = requests.get(self.gh_jwks_url, timeout=5)
        if not response.ok:
            logging.error("Failed to get GitHub's JWKS.")
            return None

        self.gh_jwks_last_fetched = now
        self.gh_jwks = response.json()["keys"]
        return self.gh_jwks

    def _decode_token(self, token: str):
        jwks = self._get_github_jwks()
        if not jwks:
            return None

        try:
            header = jwt.get_unverified_header(token)
            kid = header.get("kid")

            key: t.Optional[JsonDict] = None
            for jwk in jwks:
                if jwk.get("kid") == kid:
                    key = jwk
                    break

            if not key:
                logging.info("No matching JWK found for kid: %s", kid)
                return None

            return jwt.decode(
                token,
                key=RSAAlgorithm.from_jwk(key),
                algorithms=["RS256", "RS384", "RS512"],
                audience=settings.SERVICE_DOMAIN,
                issuer=self.gh_oidc_issuer,
                options={"require_exp": True, "verify_signature": True},
            )

        except jwt.exceptions.ExpiredSignatureError:
            logging.info("Token has expired.")
        except jwt.exceptions.InvalidAudienceError:
            logging.info("Token audience mismatch.")
        except jwt.exceptions.InvalidIssuerError:
            logging.info("Token issuer mismatch.")
        except jwt.exceptions.InvalidSignatureError:
            logging.info("Token signature is invalid.")
        except jwt.exceptions.PyJWTError as error:
            logging.info("JWT verification failed: %s", error)

        return None

    def has_permission(self, request, view):
        auth_header = request.headers.get("Authorization")
        if auth_header:
            if not auth_header.startswith("Bearer "):
                logging.info("Expected a bearer token.")
                return False

            token = auth_header.split(" ")[1]

            decoded_token = self._decode_token(token)
            return decoded_token is not None

        return False
