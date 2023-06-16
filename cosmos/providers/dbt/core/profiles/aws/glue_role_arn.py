"Maps Aws connections to dbt profiles."
from __future__ import annotations

from logging import getLogger
from typing import Any

from ..base import BaseProfileMapping

logger = getLogger(__name__)


class AWSGlueProfileMapping(BaseProfileMapping):
    """
        Maps Airflow Aws connections to Glue dbt profiles.

        https://docs.getdbt.com/docs/core/connect-data-platform/glue-setup
        https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/connections/aws.html
        https://github.com/aws-samples/dbt-glue
    """
    airflow_connection_type: str = "aws"
    is_community: bool = True

    # Reference link:
    required_fields = [
        "role_arn",
        "region",
        "workers",
        "worker_type",
        "schema",
        "session_provisioning_timeout_in_seconds",
        "location",
    ]

    airflow_param_mapping = {
        "role_arn": "extra.role_arn",
        "region": "extra.region_name",
    }

    @property
    def profile(self) -> dict[str, Any | None]:
        """
        Return a dbt Aws glue profile based on the Aws connection.
        """
        profile_vars = {
            "type": "glue",
            "role_arn": self.role_arn,
            "region": self.region,
            **self.profile_args,
        }
        # remove any null values
        return self.filter_null(profile_vars)
