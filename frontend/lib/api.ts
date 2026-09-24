const API_URL =
  typeof window === "undefined"
    ? process.env.API_URL
    : process.env.NEXT_PUBLIC_API_URL;

export type InventoryItem = {
  id: string;
  name: string;
  serial_number: string;
  category: string | null;
  category_name: string | null;
  location: string | null;
  location_name: string | null;
  quantity: number;
  status: string;
  notes: string;
  created_at: string;
  updated_at: string;
};

export async function getInventoryItems(): Promise<InventoryItem[]> {
  const response = await fetch(`${API_URL}/items/`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to fetch inventory.");
  }

  return response.json();
}