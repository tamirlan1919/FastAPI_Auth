// «Компонент» страницы корзины. Отвечает за: показать позиции и итог.
import { itemPrice } from '../pricing';
import { cartStore } from '../store/cart.store';

export function renderCartPage(): void {
  console.log('📄 Страница корзины:');
  for (const item of cartStore.getItems()) {
    console.log(`   ${item.pizza.name} (${item.size}) × ${item.qty} = ${itemPrice(item)} ₽`);
  }
  console.log(`   Итого: ${cartStore.total()} ₽`);
}
