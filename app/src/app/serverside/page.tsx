import { appRouter } from "../api/trpc/router";

/** This is a React Server Component */
export default async function RSCPage() {
  const caller = appRouter.createCaller({});
  // call the tRPC endpoint
  const message = await caller.forecast.get();

  // we render this output on the server
  return (
    <main className="flex min-h-screen items-center justify-center bg-gradient-to-tr to-blue-400 from-green-500 p-10">
      <div className="w-max">
        <div className="animate-typing overflow-hidden whitespace-nowrap border-r-4 border-r-white pr-5 text-5xl text-white font-bold">
          {message}
        </div>
      </div>
    </main>
  );
}
