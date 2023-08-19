import Message from "./message";

export default function Home() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-gradient-to-tr to-blue-400 from-green-500 p-10">
      <div className="w-max">
        <Message />
      </div>
    </main>
  );
}
