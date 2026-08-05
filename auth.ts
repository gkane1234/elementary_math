import NextAuth from "next-auth";
import Google from "next-auth/providers/google";

const googleConfigured = Boolean(
  process.env.AUTH_GOOGLE_ID && process.env.AUTH_GOOGLE_SECRET,
);

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: googleConfigured
    ? [
        Google({
          clientId: process.env.AUTH_GOOGLE_ID!,
          clientSecret: process.env.AUTH_GOOGLE_SECRET!,
          // Required for oauth4webapi issuer checks (RFC 9207 / OIDC).
          issuer: "https://accounts.google.com",
        }),
      ]
    : [],
  // Avoid MissingSecret crashes when auth env vars are not set yet.
  secret: process.env.AUTH_SECRET ?? "unconfigured-auth-secret",
  session: {
    strategy: "jwt",
  },
  pages: {
    signIn: "/signin",
  },
  callbacks: {
    jwt({ token, account, profile }) {
      if (account?.provider === "google" && profile && "sub" in profile && profile.sub) {
        token.sub = profile.sub;
      }
      return token;
    },
    session({ session, token }) {
      if (session.user && token.sub) {
        session.user.id = token.sub;
      }
      return session;
    },
  },
  trustHost: true,
});

export function isAuthConfigured(): boolean {
  return Boolean(process.env.AUTH_SECRET && googleConfigured);
}
