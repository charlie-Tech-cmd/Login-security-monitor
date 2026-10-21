# L2E CyberGuard authentication UI

A React and Tailwind CSS registration/login interface. Start the local
development server with `npm run dev`; run the production build with
`npm run build`, and run validation tests with `npm test`.

The frontend sends JSON requests to `POST /api/auth/register` and
`POST /api/auth/login` on the current origin. Copy `.env.example` to
`.env.local` and set `VITE_API_BASE_URL` to a backend origin if the API is
hosted separately. Until a backend is connected, submission errors display a
generic frontend message. Successful feedback is shown only after a successful
response.
