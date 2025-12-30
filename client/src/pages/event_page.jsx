import { useEffect, useState } from "react";
const API_BASE = import.meta.env.VITE_API_BASE_URL;

export default function EventPage() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  async function getEventPageData() {
    try {
      setLoading(true);
      setError(null);

      const res = await fetch(`${API_BASE}/api/webhook/events`);

      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.error || "Failed to fetch data");
      }

      const webhookData = await res.json();
      setData(webhookData);
    } catch (err) {
      setError(err.message || "Failed to fetch data");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    getEventPageData();
  }, []);

  return (
    <div className="max-w-4xl mx-auto mt-12 bg-white rounded-lg shadow border border-purple-300">
      <div className="px-6 py-4 border-b border-purple-300">
        <h2 className="text-lg font-semibold text-purple-700">
          Webhook Events
        </h2>
        <p className="text-sm text-gray-500">
          Incoming webhook data processed by the system
        </p>
      </div>

      <div className="px-6 py-3 border-b border-purple-200">
        <div className="px-6 py-2 text-xs text-purple-600 bg-purple-50 border-b border-purple-200">
          Note: The first request may take up to ~1 minute while the service
          initializes.
        </div>

        <button
          onClick={async () => {
            await fetch(`${API_BASE}/api/webhook/process`, {
              method: "POST",
            });
            getEventPageData(); // refresh after retry
          }}
          className="px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700 text-sm"
        >
          Retry Errors
        </button>
      </div>

      {loading && (
        <div className="p-6 text-center text-gray-500">Loading events…</div>
      )}

      {error && <div className="p-6 text-center text-red-600">{error}</div>}

      {!loading && !error && data.length === 0 && (
        <div className="p-6 text-center text-gray-500">
          No events received yet
        </div>
      )}

      {!loading && !error && data.length > 0 && (
        <div className="overflow-x-auto">
          <table className="w-full border-collapse">
            <thead className="bg-purple-100 text-purple-800 text-sm uppercase">
              <tr>
                <th className="px-4 py-3 text-left border-b border-purple-300">
                  ID
                </th>
                <th className="px-4 py-3 text-left border-b border-purple-300">
                  Name
                </th>
                <th className="px-4 py-3 text-left border-b border-purple-300">
                  Phone
                </th>
                <th className="px-4 py-3 text-left border-b border-purple-300">
                  Created At
                </th>
                <th className="px-4 py-3 text-left border-b border-purple-300">
                  Status
                </th>
              </tr>
            </thead>

            <tbody className="text-sm text-gray-700">
              {data.map((d) => (
                <tr key={d.id} className="hover:bg-purple-50 transition">
                  <td className="px-4 py-3 border-b border-purple-200">
                    {d.id}
                  </td>
                  <td className="px-4 py-3 border-b border-purple-200">
                    {d.name}
                  </td>
                  <td className="px-4 py-3 border-b border-purple-200">
                    {d.phone}
                  </td>
                  <td className="px-4 py-3 border-b border-purple-200">
                    {new Date(d.created_at).toLocaleString()}
                  </td>
                  <td
                    className={`px-4 py-3 border-b border-purple-200 font-medium ${
                      d.status.includes("error")
                        ? "text-red-600"
                        : d.status.includes("processing")
                        ? "text-yellow-600"
                        : "text-green-600"
                    }`}
                  >
                    {d.status}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
