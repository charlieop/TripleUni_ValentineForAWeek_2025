export default defineNuxtRouteMiddleware((to) => {
  const { getOpenId } = useStore();
  const openId = getOpenId();
  if (to.path === "/login" || to.path === "/login/") {
    if (openId) {
      return navigateTo("/");
    }
    return;
  }

  if (!openId) {
    return navigateTo("/login");
  }
});
