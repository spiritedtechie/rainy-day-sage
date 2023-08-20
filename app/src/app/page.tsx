import { appRouter } from "./api/trpc/router";

const getForecast = async () => {
  const caller = appRouter.createCaller({});

  try {
    const forecast = await caller.forecast.get();
    return [
      {
        image: "/weatherperson.png",
        image_alt_text: "Weather Person",
        text: forecast.summary,
      },
      {
        image: "/yoga.png",
        image_alt_text: "Yoga Person",
        text: forecast["inspiring-message"],
      },
    ];
  } catch (e) {
    return [
      {
        image: "/error.png",
        image_alt_text: "Error",
        text: "Sorry! I am unable to retrieve the weather forecast right now.",
      },
    ];
  }
};

/** This is a React Server Component */
export default async function Home() {
  // we render this output on the server
  const messages = await getForecast();

  return (
    <main className="flex min-h-screen items-center justify-center bg-gradient-to-tr to-blue-400 from-green-500 p-5">
      <div className="w-max">
        {messages.map((message) => (
          <div className="md:flex rounded-xl shadow-lg border border-gray-500 p-10 mt-10">
            <img
              src={message.image}
              alt={message.image_alt_text}
              className="w-20 h-20 mx-auto md:mr-10"
            />
            <blockquote className="mt-5 md:mt-0">
              <p className="text-lg text-white font-medium font-bold">
                "{message.text}"
              </p>
            </blockquote>
          </div>
        ))}
      </div>
    </main>
  );
}
