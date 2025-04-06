module.exports = {
    content: ["./frontend/templates/**/*.html", "../frontend/static/**/*.css"],
    theme: {
      extend: {},
    },
    plugins: [],
    safelist: [
        {
          pattern: /./,
        },
      ],
  };