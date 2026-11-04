// Общие типы приложения — «словарь» PizzaHub. Только описания, никакой логики.

export interface Pizza {
  id: number;
  name: string;
  price: number;      // рубли, для размера M
  isVegan: boolean;
  createdAt: Date;
}

export type Size = 'S' | 'M' | 'L';

export interface CartItem {
  pizza: Pizza;
  size: Size;
  qty: number;
}

export interface Order {
  id: string;
  items: CartItem[];
  address: string;
  phone: string;
  comment: string;
  contactless: boolean;
  promoCode: string | null;
  total: number;
  createdAt: Date;
}
