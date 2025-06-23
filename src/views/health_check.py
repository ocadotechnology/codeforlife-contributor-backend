"""TODO: delete"""

from codeforlife.views.health_check import HealthCheck, HealthCheckDetailList
from codeforlife.views.health_check import HealthCheckView as _HealthCheckView
from codeforlife.views.health_check import Request, Site, apps, settings


# pylint: disable-next=missing-class-docstring
class HealthCheckView(_HealthCheckView):
    def get_django_worker_health_check(self, request: Request) -> HealthCheck:
        """Check the health of the django worker process."""
        health_check_details = HealthCheckDetailList("django")

        ready = apps.ready
        health_check_details.append(
            name="ready",
            description=str(ready),
            health="healthy" if ready else "startingUp",
        )

        apps_ready = apps.apps_ready
        health_check_details.append(
            name="apps_ready",
            description=str(apps_ready),
            health="healthy" if apps_ready else "startingUp",
        )

        models_ready = apps.models_ready
        health_check_details.append(
            name="models_ready",
            description=str(models_ready),
            health="healthy" if models_ready else "startingUp",
        )

        if settings.DB_ENGINE == "postgresql":
            host = request.get_host()
            # if not host.endswith(":8080"):
            site_exists = Site.objects.filter(domain=host).exists()
            health_check_details.append(
                name="site_exists",
                description=str(site_exists),
                health="healthy" if site_exists else "unhealthy",
            )

        health_status = self.resolve_health_status(
            *health_check_details.health_statuses
        )

        return HealthCheck(
            health_status=health_status,
            additional_info="[django] "
            + (
                "All healthy."
                if health_status == "healthy"
                else "Not healthy. See details for more info."
            ),
            details=health_check_details,
        )
