Changelog
=========

1.1.0a1 (2023-08-16)
--------------------

Feature (pending documentation!)
* Support dbt global flags (via dbt_cmd_global_flags in operator_args) by @tatiana in #469

Enhancements
* Hide sensitive field when using BigQuery keyfile_dict profile mapping by @jbandoro in #471

Bug fixes
* Fix bug on select node add exclude selector subset ids logic by @jensenity in #463
* Refactor dbt ls to run from a temporary directory, to avoid Read-only file system errors during DAG parsing, by @tatiana in #414

Others
* Docs: Fix RenderConfig load argument by @jbandoro in #466
* Enable CI integration tests from external forks by @tatiana in #458
* Improve CI tests runtime by @tatiana in #457
* Change CI to run coverage after tests pass by @tatiana in #461
* Fix forks code revision in code coverage by @tatiana in #472
* [pre-commit.ci] pre-commit autoupdate by @pre-commit-ci in #467

1.0.5 (2023-08-09)
------------------

Enhancements
* Improve logs to include astornomer-cosmos identifier by @tatiana in #450
* Support OAuth authentication for Big Query by @MonideepDe in #431

Bug fixes
* Fix selector for config tags by @javihernovoa in #441
* Fix BigQuery keyfile_dict mapping for connection created from webserver UI by @jbandoro in #449

Others
* [pre-commit.ci] pre-commit autoupdate by @pre-commit-ci in #446
* Resolve MyPy errors when adding Airflow pre-commit dependency by @abhi12mohan in #434


1.0.0 (2022-12-14)
-------------------

* Initial release, with the following **6** workflow Operators/Parsers:

.. list-table::
   :header-rows: 1

   * - Operator/Sensor Class
     - Import Path
     - Example DAG

   * - ``DBTTestOperator``
     - .. code-block:: python

        from cosmos.providers.dbt.core.operators import DBTBaseOperator
     - N/A

   * - ``DBTSeedOperator``
     - .. code-block:: python

        from cosmos.providers.dbt.core.operators import DBTSeedOperator
     - `Example DAG <https://github.com/astronomer/astronomer-cosmos/blob/1.0.0/examples/dags/extract_dag.py>`__

   * - ``DBTRunOperator``
     - .. code-block:: python

        from cosmos.providers.dbt.core.operators import DBTRunOperator
     - N/A

   * - ``DBTTestOperator``
     - .. code-block:: python

        from cosmos.providers.dbt.core.operators import DBTTestOperator
     - N/A

   * - ``DbtDag``
     - .. code-block:: python

        from cosmos.providers.dbt.core.dag import DbtDag
     - `Example DAG <https://github.com/astronomer/astronomer-cosmos/blob/1.0.0/examples/dags/attribution-playbook.py>`__

   * - ``DbtTaskGroup``
     - .. code-block:: python

        from cosmos.providers.dbt.core.dag import DbtTaskGroup
     - `Example DAG <https://github.com/astronomer/astronomer-cosmos/blob/1.0.0/examples/dags/jaffle_shop.py>`__
