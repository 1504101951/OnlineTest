export function formatDateToMinute(date) {
    if (!date) return '';

    // 使用moment格式化日期
    return moment.utc(date).format('YYYY年M月D日 HH时mm分');
}

export function formatDateToSecond(date)
{
  return date.format("YYYY-MM-DD HH:mm:ss")
}