# question-answering-assistant-33453-33463

IMPORTANT: Supabase Secret Configuration

To allow the backend to fetch OPENAI_API_KEY from Supabase when not present in the environment, set:

- SUPABASE_URL=https://<your-project-ref>.supabase.co
- SUPABASE_SERVICE_ROLE_KEY=<service role key> (server-side only)
- SUPABASE_SECRET_PASSPHRASE=<strong random secret>
- (Optional) OPENAI_API_KEY=<your key> — if set, backend will use this directly without contacting Supabase.

Then re-run the Supabase configuration agent to create the secret store and store OPENAI_API_KEY securely.