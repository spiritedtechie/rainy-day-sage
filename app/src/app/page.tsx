import { appRouter } from "./api/trpc/router";
import Image from "next/image";

/** This is a React Server Component */
export default async function RSCPage() {
  const caller = appRouter.createCaller({});
  // call the tRPC endpoint
  const forecast = await caller.forecast.get();

  // we render this output on the server
  return (
    <main className="flex min-h-screen items-center justify-center bg-gradient-to-tr to-blue-400 from-green-500 p-5">
      <div className="w-max">
        <div className="md:flex rounded-xl shadow-lg border border-gray-500 p-10 mt-10">
          <img
            src="/weatherperson.png"
            alt="Weather person"
            className="w-20 h-20 mx-auto md:mr-10"
          />
          <blockquote className="mt-5 md:mt-0">
            <p className="text-lg text-white font-medium font-bold">
              "{forecast.summary}"
            </p>
          </blockquote>
        </div>

        <div className="md:flex rounded-xl shadow-lg border border-gray-500 p-10 mt-10">
          <img
            src="/yoga.png"
            alt="Yoga person"
            className="w-20 h-20 mx-auto md:mr-10"
          />
          <blockquote className="mt-5 md:mt-0">
            <p className="text-lg text-white font-medium font-bold">
              "{forecast["inspiring-message"]}"
            </p>
          </blockquote>
        </div>
      </div>
    </main>
  );
}
