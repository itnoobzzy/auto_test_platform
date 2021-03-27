/*  用export把方法暴露出来  */

/*  设置cookie  */
// eslint-disable-next-line camelcase
export function setCookie (c_name, value, expire) {
  console.log('cook打印', c_name, value, expire)
  let date = new Date()
  date.setSeconds(date.getSeconds() + expire)
  // eslint-disable-next-line camelcase
  document.cookie = c_name + '=' + escape(value) + '; expires=' + date.toGMTString()
}

/* 获取cookie */
export function getCookie(c_name) {
  let cookieName = encodeURIComponent(c_name) + '=',
    cookieStart = document.cookie.indexOf(cookieName),
    cookieValue = null;
  if (cookieStart > -1) {
    let cookieEnd = document.cookie.indexOf(';', cookieStart);
    if (cookieEnd === -1) {
      cookieEnd = document.cookie.length;
    }
    cookieValue = unescape(document.cookie.substring(cookieStart + cookieName.length, cookieEnd)).replace(/\'/g, '');
  }
  return cookieValue;
}

/* 删除cookie */
export function delCookie(c_name) {
  setCookie(c_name, '', -1)
}
