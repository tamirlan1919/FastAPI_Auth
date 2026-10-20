// Имитация платёжного сервиса. Отвечает за: «списать» деньги или отказать.
const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

export async function payWithCard(amount: number): Promise<string> {
  await sleep(200);
  if (amount > 5000) throw new Error('Банк отклонил платёж: недостаточно средств');
  return `pay_${Date.now()}`;
}
