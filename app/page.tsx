import { redirect } from "next/navigation";
import { LandingPage } from "@/components/LandingPage";
import { generatorRedirectPath } from "@/lib/landing";

type HomeSearchParams = Record<string, string | string[] | undefined>;

export default async function HomePage({
  searchParams,
}: {
  searchParams: Promise<HomeSearchParams>;
}) {
  const target = generatorRedirectPath(await searchParams);
  if (target) redirect(target);
  return <LandingPage />;
}
