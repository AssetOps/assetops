import { getStockLevels } from "@/lib/api";

export default async function InventoryPage() {
  const stockLevels = await getStockLevels();

  return (
    <main className="p-8">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Inventory</h1>

          <p className="text-gray-500">
            Manage products and stock across locations.
          </p>
        </div>

        <button className="rounded-lg bg-black px-4 py-2 text-white">
          Add Product
        </button>
      </div>

      <div className="overflow-hidden rounded-xl border">
        <table className="w-full">
          <thead className="border-b bg-gray-50">
            <tr>
              <th className="p-4 text-left">Product</th>
              <th className="p-4 text-left">SKU</th>
              <th className="p-4 text-left">Category</th>
              <th className="p-4 text-left">Location</th>
              <th className="p-4 text-left">Quantity</th>
            </tr>
          </thead>

          <tbody>
            {stockLevels.map((stock) => (
              <tr key={stock.id} className="border-b">
                <td className="p-4 font-medium">{stock.product_name}</td>

                <td className="p-4">{stock.product_sku}</td>

                <td className="p-4">{stock.category_name}</td>

                <td className="p-4">{stock.location_name}</td>

                <td className="p-4">{stock.quantity_on_hand}</td>
              </tr>
            ))}
          </tbody>
        </table>

        {stockLevels.length === 0 && (
          <div className="p-10 text-center text-gray-500">
            No inventory yet.
          </div>
        )}
      </div>
    </main>
  );
}
