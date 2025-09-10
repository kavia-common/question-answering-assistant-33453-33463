# Supabase Configuration and Secret Management

This project integrates with Supabase for secure secret storage and optional database features. We will use the Supabase "encrypted secret_store" table to store and retrieve secrets such as OPENAI_API_KEY.

Status: Partial – Supabase credentials are not present in the environment, so database operations (list tables, create tables, run SQL) were not executed yet. Once credentials are provided, re-run this agent to complete the setup steps in the "Next Steps" section.

## Required Environment Variables

Provide the Supabase credentials to enable tool-based configuration:

- SUPABASE_URL=https://<your-project-ref>.supabase.co
- SUPABASE_ANON_KEY=<your anon public key>
- SUPABASE_SERVICE_ROLE_KEY=<your service role key> (server-side only; do NOT expose to frontend)

Optionally supported aliases (if your environment uses them):
- APP_SUPABASE_URL / APP_SUPABASE_ANON_KEY
- REACT_APP_SUPABASE_URL / REACT_APP_SUPABASE_ANON_KEY

At minimum, this backend needs either:
- SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY (preferred for server)
or
- SUPABASE_URL + SUPABASE_ANON_KEY (read-mostly operations).

For OpenAI:
- OPENAI_API_KEY: If not set in the environment, the backend can fetch it from Supabase Secret Store.

## Planned Supabase Setup (to run when credentials are available)

The following operations will be executed by the agent using Supabase tools:

1) Inspect current database:
   - SupabaseTool_list_tables

2) Install encrypted secret store (idempotent):
   - SupabaseTool_create_secret_store

3) Store OPENAI_API_KEY (upsert, encrypted):
   - SupabaseTool_set_secret(key="OPENAI_API_KEY", value="<from current env>", passphrase="<project passphrase>")

4) Configure RLS policies as needed:
   - Using SupabaseTool_run_sql to ensure secret_store is admin-only (by default it is internal-use; no public access).

5) Verification:
   - SupabaseTool_get_secret(key="OPENAI_API_KEY", passphrase="<project passphrase>") to confirm retrieval.

Note: The passphrase used for pgp_sym_encrypt is maintained outside of the database, in a server-only environment variable:
- SUPABASE_SECRET_PASSPHRASE=<a strong random secret>

This passphrase is required to encrypt/decrypt secret values.

## How the Backend Uses the Secret

The backend attempts to read OPENAI_API_KEY in the following order:
1. Directly from environment var OPENAI_API_KEY
2. From Supabase Secret Store entry "OPENAI_API_KEY" using SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY and SUPABASE_SECRET_PASSPHRASE

If both are missing, the backend returns 503 on /api/qa/ask/ with a helpful message.

## App Integration Notes (Django)

- No direct Supabase client is required for basic REST endpoints. We use the Supabase Secret Store HTTP RPC via tool in setup phase, but at runtime we can optionally retrieve the secret via a simple PostgREST call or a server-side utility if desired.
- For this project, the secret retrieval is performed lazily only if OPENAI_API_KEY is not present in the environment.

## Security

- Never commit OPENAI_API_KEY to source control.
- Do not expose SUPABASE_SERVICE_ROLE_KEY to the client-side.
- Include your deployment URLs in the Supabase Auth > URL Configuration if you later use Supabase Auth.

## Next Steps (Action Items)

1) Add the following environment variables to the qa_backend runtime:
   - SUPABASE_URL
   - SUPABASE_SERVICE_ROLE_KEY (or ANON_KEY if you cannot use service role)
   - SUPABASE_SECRET_PASSPHRASE (a strong random string)

2) Optionally set OPENAI_API_KEY in env now. If you omit it, the agent will prompt to store it in Supabase Secret Store on the next run.

3) Re-run this Supabase configuration agent. It will:
   - Create/verify the secret_store
   - Upsert OPENAI_API_KEY into secret_store (if provided)
   - Configure strict policies
   - Document success in this file

## Troubleshooting

- If you see "No valid Supabase credentials found" during setup, verify that the variables are exported to the environment seen by the agent.
- Ensure network access to your Supabase project domain is allowed from your environment.

Once credentials are available, I will complete the database and secret-store steps and update this file with the results.
