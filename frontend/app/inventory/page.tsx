type InventoryItem = {
  id: string;
  name: string;
  serial_number: string;
  quantity: number;
  status: string;
  notes: string;
};

async function getItems(): Promise<InventoryItem[]> {
  const apiUrl =
    process.env.API_URL ??
    process.env.NEXT_PUBLIC_API_URL ??
    "http://backend:8000/api";

  const response = await fetch(`${apiUrl}/items/`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to load inventory");
  }

  return response.json();
}

export default async function InventoryPage() {
  const items = await getItems();

  return (
    <main className="p-8">
      <h1 className="mb-6 text-3xl font-bold">Inventory</h1>

      <div className="overflow-hidden rounded-lg border">
        <table className="w-full">
          <thead>
            <tr className="border-b">
              <th className="p-4 text-left">Name</th>
              <th className="p-4 text-left">Serial Number</th>
              <th className="p-4 text-left">Quantity</th>
              <th className="p-4 text-left">Status</th>
            </tr>
          </thead>

          <tbody>
            {items.map((item) => (
              <tr key={item.id} className="border-b">
                <td className="p-4">{item.name}</td>
                <td className="p-4">
                  {item.serial_number || "Not set"}
                </td>
                <td className="p-4">{item.quantity}</td>
                <td className="p-4 capitalize">{item.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  );
}