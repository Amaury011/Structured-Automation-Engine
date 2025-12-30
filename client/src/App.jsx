import EventPage from "./pages/event_page.jsx";

function App() {
  return (
    <div className="min-h-screen w-full bg-purple-200">
      {/* Header */}
      <header className="w-full border-b border-purple-400 bg-purple-300">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <h1 className="text-2xl font-bold text-purple-800">
            Google Data Sync
          </h1>
          <p className="text-sm text-purple-700">
            Webhook syncing for Sheets & Contacts
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="px-6 py-10">
        <EventPage />
      </main>
    </div>
  );
}

export default App;
