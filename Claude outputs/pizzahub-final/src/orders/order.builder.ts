// BUILDER. Отвечает за: пошагово собрать заказ и проверить его перед созданием.
import { randomUUID } from 'node:crypto';
import { calcTotal } from '../pricing';
import type { CartItem, Order } from '../types';

export const newOrderId = (): string => randomUUID().slice(0, 8);

export class OrderBuilder {
  private items: CartItem[] = [];
  private address = '';
  private phone = '';
  private comment = '';
  private contactless = false;
  private promoCode: string | null = null;

  // каждый шаг возвращает this — поэтому можно писать цепочкой
  fromCart(items: CartItem[]) { this.items = items; return this; }
  to(address: string) { this.address = address.trim(); return this; }
  withPhone(phone: string) { this.phone = phone.replace(/[\s()-]/g, ''); return this; }
  withComment(comment: string) { this.comment = comment; return this; }
  contactlessDelivery() { this.contactless = true; return this; }
  withPromo(code: string | null) { this.promoCode = code; return this; }

  // build() — единственное место, где заказ может появиться. И только валидным.
  build(): Order {
    if (this.items.length === 0) throw new Error('Корзина пуста');
    if (this.address.length < 5) throw new Error('Не указан адрес доставки');
    if (!/^\+7\d{10}$/.test(this.phone)) throw new Error('Телефон в формате +7XXXXXXXXXX');

    return {
      id: newOrderId(),
      items: this.items,
      address: this.address,
      phone: this.phone,
      comment: this.comment,
      contactless: this.contactless,
      promoCode: this.promoCode,
      total: calcTotal(this.items, this.promoCode),
      createdAt: new Date(),
    };
  }
}
