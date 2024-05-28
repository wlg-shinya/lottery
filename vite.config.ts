import { defineConfig, loadEnv } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default ({ mode }) => {
  process.env = { ...process.env, ...loadEnv(mode, process.cwd()) };

  return defineConfig({
    plugins: [vue()],
    define: {
      __APP_VERSION__: JSON.stringify(process.env.npm_package_version),
    },
    esbuild: {
      keepNames: true,
    },
  });
};
