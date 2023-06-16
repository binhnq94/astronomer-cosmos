from unittest.mock import patch

import pytest
from airflow.models.connection import Connection

from cosmos.providers.dbt.core.profiles import get_profile_mapping
from cosmos.providers.dbt.core.profiles.glue.aws_role_arn import (
    AWSRoleARNProfileMapping,
)


@pytest.fixture()
def mock_aws_connection():  # type: ignore
    """
    Sets the connection as an environment variable.
    """
    conn = Connection(
        conn_id="my_aws_connection",
        conn_type="aws",
        login="my_user",
        password="my_password",
        extra={
            "role_arn": "arn:aws:iam::1234567890:role/GlueInteractiveSessionRole",
            "region_name": "eu-central-1",
        },
    )

    with patch("airflow.hooks.base.BaseHook.get_connection", return_value=conn):
        yield conn


def test_connection_claiming() -> None:
    """
    Tests that the Aws profile mapping claims the correct connection type.
    """
    # should only claim when:
    # - conn_type == aws
    # and the following exist:
    # - role_arn
    # - extra.region_name
    # - workers
    # - worker_type
    # - schema
    # - session_provisioning_timeout_in_seconds
    # - location

    connection_attributes = {
        "conn_id": "my_aws_connection",
        "conn_type": "aws",
        "login": "my_user",
        "password": "my_password",
    }

    extra_potential_values = {
        "role_arn": "arn:aws:iam::1234567890:role/GlueInteractiveSessionRole",
        "region_name": "eu-central-1",
    }

    profile_args_potential_values = {
        "workers": 2,
        "worker_type": "G1.X",
        "schema": "my_schema",
        "session_provisioning_timeout_in_seconds": 120,
        "location": "s3a://my_bucket",
    }

    # if we're missing any of the values in extra, it shouldn't claim
    for key in extra_potential_values:
        values = extra_potential_values.copy()
        del values[key]
        conn = Connection(**connection_attributes, extra=values)  # type: ignore

        print("testing with extra:", values)

        profile_mapping = AWSRoleARNProfileMapping(conn, profile_args_potential_values)
        assert not profile_mapping.can_claim_connection()

    # if we're missing any of the values in profile args, it shouldn't claim
    for key in profile_args_potential_values:
        values = profile_args_potential_values.copy()
        del values[key]
        conn = Connection(**connection_attributes, extra=extra_potential_values)  # type: ignore

        print("testing with profile_args", values)

        profile_mapping = AWSRoleARNProfileMapping(conn, values)
        assert not profile_mapping.can_claim_connection()

    # if we have them all, it should claim
    conn = Connection(**connection_attributes, extra=extra_potential_values)  # type: ignore
    profile_mapping = AWSRoleARNProfileMapping(conn, profile_args_potential_values)
    assert profile_mapping.can_claim_connection()


def test_profile_mapping_selected(
    mock_aws_connection: Connection,
) -> None:
    """
    Tests that the correct profile mapping is selected.
    """
    profile_mapping = get_profile_mapping(
        mock_aws_connection.conn_id,
        {
            "workers": 2,
            "worker_type": "G1.X",
            "schema": "my_schema",
            "session_provisioning_timeout_in_seconds": 120,
            "location": "s3a://my_bucket",
        },
    )
    assert isinstance(profile_mapping, AWSRoleARNProfileMapping)


def test_profile_args(
    mock_aws_connection: Connection,
) -> None:
    """
    Tests that the profile values get set correctly.
    """
    profile_mapping = get_profile_mapping(
        mock_aws_connection.conn_id,
        profile_args={
            "workers": 2,
            "worker_type": "G1.X",
            "schema": "my_schema",
            "session_provisioning_timeout_in_seconds": 120,
            "location": "s3a://my_bucket",
        },
    )
    assert profile_mapping.profile_args == {
        "workers": 2,
        "worker_type": "G1.X",
        "schema": "my_schema",
        "session_provisioning_timeout_in_seconds": 120,
        "location": "s3a://my_bucket",
    }

    assert profile_mapping.profile == {
        "type": "glue",
        "role_arn": "arn:aws:iam::1234567890:role/GlueInteractiveSessionRole",
        "region": "eu-central-1",
        "workers": 2,
        "worker_type": "G1.X",
        "schema": "my_schema",
        "session_provisioning_timeout_in_seconds": 120,
        "location": "s3a://my_bucket",
    }


def test_profile_args_overrides(
    mock_aws_connection: Connection,
) -> None:
    """
    Tests that you can override the profile values.
    """
    profile_mapping = get_profile_mapping(
        mock_aws_connection.conn_id,
        profile_args={
            "role_arn": "my_role_arn_override",
            "region": "my_region_override",
            "workers": 2,
            "worker_type": "G1.X",
            "schema": "my_schema",
            "session_provisioning_timeout_in_seconds": 120,
            "location": "s3a://my_bucket",
        },
    )
    assert profile_mapping.profile_args == {
        "role_arn": "my_role_arn_override",
        "region": "my_region_override",
        "workers": 2,
        "worker_type": "G1.X",
        "schema": "my_schema",
        "session_provisioning_timeout_in_seconds": 120,
        "location": "s3a://my_bucket",
    }

    assert profile_mapping.profile == {
        "type": "glue",
        "role_arn": "my_role_arn_override",
        "region": "my_region_override",
        "workers": 2,
        "worker_type": "G1.X",
        "schema": "my_schema",
        "session_provisioning_timeout_in_seconds": 120,
        "location": "s3a://my_bucket",
    }
