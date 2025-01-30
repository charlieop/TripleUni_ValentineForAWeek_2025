const { getOpenId } = useStore();

export default defineNuxtRouteMiddleware((to, from) => {
  const openId = getOpenId();
  if (to.path === "/login") {
    if (openId) {
      return navigateTo("/");
    }
    return;
  }
  if (!openId) {
    return navigateTo("/login");
  }
});
