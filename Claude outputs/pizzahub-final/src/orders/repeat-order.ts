// PROTOTYPE. Отвечает за: сделать новый заказ как КОПИЮ старого («Повторить заказ»).
import type { Order } from '../types';
import { newOrderId } from './order.builder';

type OrderChanges = Partial<Pick<Order, 'address' | 'comment' | 'contactless'>>;

export function repeatOrder(original: Order, changes: OrderChanges = {}): Order {
  const copy = structuredClone(original);   // ГЛУБОКАЯ копия: вложенные items тоже новые
  return {
    ...copy,
    ...changes,
    id: newOrderId(),          // у копии свой номер
    createdAt: new Date(),     // и своё время
  };
}
