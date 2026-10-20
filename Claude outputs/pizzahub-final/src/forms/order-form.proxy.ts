// PROXY. Отвечает за: стоять «на входе» в данные формы — проверять каждое изменение
// и сообщать интерфейсу, что пора перерисоваться.

export interface OrderForm {
  address: string;
  phone: string;
  qty: number;
}

type Rule = (value: unknown) => string | null;   // null = всё хорошо, строка = текст ошибки

const rules: Record<keyof OrderForm, Rule> = {
  address: (v) => (typeof v === 'string' && v.trim().length >= 5 ? null : 'адрес слишком короткий'),
  phone: (v) => (typeof v === 'string' && /^\+7\d{10}$/.test(v) ? null : 'нужен формат +7XXXXXXXXXX'),
  qty: (v) => (Number.isInteger(v) && (v as number) >= 1 && (v as number) <= 20 ? null : 'можно от 1 до 20 пицц'),
};

export function createOrderForm(onChange: (form: OrderForm) => void): OrderForm {
  const data: OrderForm = { address: '', phone: '', qty: 1 };

  return new Proxy(data, {
    set(target, prop, value) {
      const rule = rules[prop as keyof OrderForm];
      if (!rule) throw new Error(`Неизвестное поле формы: ${String(prop)}`);

      const error = rule(value);
      if (error) throw new Error(`${String(prop)}: ${error}`);   // охранник не пустил

      Reflect.set(target, prop, value);                          // пропустили к оригиналу
      onChange({ ...target });                                   // «перерисуй форму»
      return true;
    },
  });
}
