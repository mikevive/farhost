return {
  "nvimtools/none-ls.nvim",
  dependencies = {
    "nvimtools/none-ls-extras.nvim",
  },
  config = function()
    local null_ls = require("null-ls")

    local formatting = null_ls.builtins.formatting
    local diagnostics = null_ls.builtins.diagnostics

    local function has_eslint_config(utils)
      return utils.root_has_file({
        ".eslintrc",
        ".eslintrc.cjs",
        ".eslintrc.js",
        ".eslintrc.json",
        "eslint.config.cjs",
        "eslint.config.js",
        "eslint.config.mjs",
      })
    end

    null_ls.setup({
      sources = {
        -- lua
        formatting.stylua,
        -- typescript
        formatting.prettierd,
        require("none-ls.code_actions.eslint_d").with({ condition = has_eslint_config }),
        require("none-ls.diagnostics.eslint_d").with({ condition = has_eslint_config }),
        require("none-ls.formatting.eslint_d").with({ condition = has_eslint_config }),
        -- python
        formatting.black,
        formatting.isort,
        diagnostics.mypy,
        diagnostics.pylint,
        -- ruby
        formatting.rubocop,
        diagnostics.rubocop,
      },
    })

    vim.keymap.set("n", "<leader>bf", vim.lsp.buf.format, {})
  end,
}
