import js from '@eslint/js';
import prettier from 'eslint-config-prettier';
import astro from 'eslint-plugin-astro';
import tseslint from 'typescript-eslint';

export default [
    { ignores: ['dist/**', '.astro/**'] },
    js.configs.recommended,
    ...tseslint.configs.recommended,
    ...astro.configs['flat/recommended'],
    prettier,
];
