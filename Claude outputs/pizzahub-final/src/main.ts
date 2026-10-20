// Точка входа. Здесь только СЦЕНАРИЙ: что делает пользователь. Вся логика — в модулях.
import { getMenu } from './api/pizza.api';
import { getRequestCount } from './api/fake-backend';
import { checkout } from './checkout/checkout.facade';
import { createOrderForm } from './forms/order-form.proxy';
import { notify } from './notifications/toast.factory';
import { repeatOrder } from './orders/repeat-order';
import { cartStore } from './store/cart.store';
import { renderCartPage } from './ui/cart-page';
import { renderHeader } from './ui/header';

console.log('🍕 PizzaHub\n');

// 1. Меню: Adapter + Decorator
const menu = await getMenu();
menu.forEach((p) => console.log(`   ${p.id}. ${p.name} — ${p.price} ₽${p.isVegan ? ' 🌱' : ''}`));
await getMenu();   // второй раз — из кеша
console.log(`   запросов к серверу: ${getRequestCount()}\n`);

// 2. Корзина: Singleton
cartStore.add(menu[0], 'L', 2);
cartStore.add(menu[1]);
renderHeader();
renderCartPage();

// 3. Форма: Proxy
const form = createOrderForm((f) => console.log('📝 форма обновилась:', f));
form.address = 'ул. Ленина, 1';
form.phone = '+79001234567';
try {
  form.qty = 100;
} catch (error) {
  notify('error', (error as Error).message);   // Factory
}

// 4. Оформление: Facade (внутри Builder + Singleton + Factory)
console.log();
const result = await checkout({ address: form.address, phone: form.phone, promoCode: 'PIZZA10' });
renderHeader();

// 5. Повтор заказа: Prototype
if (result.ok) {
  const again = repeatOrder(result.order, { address: 'ул. Пушкина, 10' });
  again.items[0].qty = 5;
  console.log(`\n🔁 Повтор №${again.id} на ${again.address}, в нём ${again.items[0].qty} шт.`);
  console.log(`   а в оригинале №${result.order.id} осталось ${result.order.items[0].qty} шт.`);
}
