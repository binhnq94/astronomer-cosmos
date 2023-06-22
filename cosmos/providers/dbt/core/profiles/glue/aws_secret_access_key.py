"Maps Aws connections to dbt profiles."
from __future__ import annotations

from logging import getLogger
from typing import Any

from ..base import BaseProfileMapping

logger = getLogger(__name__)


class AWSSecretAccessKeyProfileMapping(BaseProfileMapping):
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
        "access_key_id": "login",
        "secret_access_key": "password"
    }

    secret_fields = [
        "access_key_id",
        "secret_access_key"
    ]

    @property
    def env_vars(self) -> dict[str, str]:
        "Returns a dictionary of environment variables that should be set based on self.secret_fields."
        env_vars = {}

        for field in self.secret_fields:
            # I re-write env_var_name for BashOperator can understand.
            env_var_name = f"{self.airflow_connection_type.upper()}_{field.upper()}"
            value = self.get_dbt_value(field)
            if value is not None:
                env_vars[env_var_name] = str(value)

        return env_vars


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
