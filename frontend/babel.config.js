module.exports = {
  presets: ['module:@react-native/babel-preset'],
  plugins: [
    [
      'module-resolver',
      {
        root: ['./'],
        alias: {
          src: './src',
          components: './src/components',
          common: './src/common',
          api: './src/api',
          features: './src/features',
          navigation: './src/navigation',
          context: './src/context',
          mock: './src/mock',
        },
      },
    ],
  ],
};
