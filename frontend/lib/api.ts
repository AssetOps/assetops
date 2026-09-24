const API_URL =
  typeof window === "undefined"
    ? (process.env.API_URL ?? "http://backend:8000/api")
    : (process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api");

export type Product = {
  id: string;
  name: string;
  sku: string;
  category: string;
  category_name: string;
};

export type StockLevel = {
  id: number;
  product: string;
  product_name: string;
  product_sku: string;
  category_name: string;
  location: string;
  location_name: string;
  quantity_on_hand: string;
  last_updated: string;
};

export async function getProducts(): Promise<Product[]> {
  const response = await fetch(`${API_URL}/products/`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to fetch products.");
  }

  return response.json();
}

export async function getStockLevels(): Promise<StockLevel[]> {
  const response = await fetch(`${API_URL}/stock-levels/`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to fetch inventory.");
  }

  return response.json();
}
