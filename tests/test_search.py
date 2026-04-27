import importlib.util
import pathlib
import shutil
import subprocess
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SEARCH_PATH = ROOT / "scripts" / "search.py"

spec = importlib.util.spec_from_file_location("backend_arch_search", SEARCH_PATH)
search_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(search_module)


class BackendArchSearchTests(unittest.TestCase):
    def test_detect_domain_security(self):
        self.assertEqual(search_module.detect_domain("jwt refresh token rbac auth"), "security")

    def test_domain_search_returns_results(self):
        result = search_module.search("cursor pagination rest api", "api", 2)
        self.assertEqual(result["domain"], "api")
        self.assertGreaterEqual(result["count"], 1)
        self.assertIn("name", result["results"][0])

    def test_all_domains_return_results(self):
        queries = {
            "api": "rest cursor pagination endpoint",
            "database": "transaction index tenant repository",
            "caching": "redis ttl invalidation cache",
            "resilience": "retry timeout circuit breaker",
            "security": "jwt rbac secret validation",
            "async": "queue webhook idempotency worker",
            "observability": "logs metrics tracing audit",
            "anti-patterns": "n+1 query hardcoded secret",
        }

        for domain, query in queries.items():
            with self.subTest(domain=domain):
                result = search_module.search(query, domain, 2)
                self.assertEqual(result["domain"], domain)
                self.assertGreaterEqual(result["count"], 1)

    def test_stack_filtering(self):
        result = search_module.search_stack("transaction service", "nestjs", 3)
        self.assertEqual(result["stack"], "nestjs")
        self.assertGreaterEqual(result["count"], 1)
        self.assertTrue(all(row["stack"] == "nestjs" for row in result["results"]))

    def test_all_stacks_return_filtered_results(self):
        expected_stacks = {
            "node-express",
            "nestjs",
            "nextjs-api",
            "laravel",
            "django",
            "fastapi",
            "spring-boot",
            "go",
            "dotnet",
            "rails",
            "phoenix",
            "hono",
            "bun",
            "actix",
            "axum",
            "ktor",
        }
        self.assertTrue(expected_stacks.issubset(set(search_module.STACK_CONFIG.keys())))

        for stack in search_module.STACK_CONFIG:
            with self.subTest(stack=stack):
                result = search_module.search_stack("service validation transaction observability", stack, 5)
                self.assertEqual(result["stack"], stack)
                self.assertGreaterEqual(result["count"], 1)
                self.assertTrue(all(row["stack"] == stack for row in result["results"]))

    def test_architecture_output_contains_core_sections(self):
        output = search_module.generate_architecture(
            "multi tenant saas auth payment webhook postgres redis",
            "Multi Tenant SaaS",
        )
        self.assertIn("TARGET:", output)
        self.assertIn("ARCHITECTURE:", output)
        self.assertIn("SECURITY:", output)
        self.assertIn("OBSERVABILITY:", output)

    def test_persist_architecture_writes_master_and_service_override(self):
        try:
            temp_dir = tempfile.TemporaryDirectory()
        except FileNotFoundError as exc:
            self.skipTest(f"No writable temporary directory available: {exc}")

        with temp_dir as tmpdir:
            output = search_module.persist_architecture(
                "billing webhook payments idempotency",
                project_name="Billing API",
                service="Webhook Worker",
                output_dir=tmpdir,
            )
            master = pathlib.Path(tmpdir) / "architecture" / "billing-api" / "MASTER.md"
            service = pathlib.Path(tmpdir) / "architecture" / "billing-api" / "services" / "webhook-worker.md"

            self.assertTrue(master.exists())
            self.assertTrue(service.exists())
            self.assertIn("Persisted Files", output)

    def test_cli_list_when_node_available(self):
        if shutil.which("node") is None:
            self.skipTest("Node.js is not available")

        cli = ROOT / "cli" / "bin" / "backend-arch-pro-max.js"
        result = subprocess.run(
            ["node", str(cli), "list"],
            cwd=str(ROOT.parent),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("codex", result.stdout)


if __name__ == "__main__":
    unittest.main()
