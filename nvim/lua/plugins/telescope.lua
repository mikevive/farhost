return {
  {
    "nvim-telescope/telescope.nvim",
    tag = "0.1.6",
    dependencies = {
      "nvim-lua/plenary.nvim",
    },
    config = function()
      local builtin = require("telescope.builtin")
      vim.keymap.set("n", "<leader><space>", builtin.find_files, {})
      vim.keymap.set("n", "<leader>fg", builtin.live_grep, {})
      vim.keymap.set("n", "<leader>ld", builtin.lsp_definitions, {})
      vim.keymap.set("n", "<leader>lr", builtin.lsp_references, {})
      vim.keymap.set("n", "<leader>li", builtin.lsp_implementations, {})
      vim.keymap.set("n", "<leader>lt", builtin.lsp_type_definitions, {})
      vim.keymap.set("n", "<leader>ls", builtin.lsp_document_symbols, {})
      vim.keymap.set("n", "<leader>lw", builtin.lsp_workspace_symbols, {})
      vim.keymap.set("n", "<leader>lci", builtin.lsp_incoming_calls, {})
      vim.keymap.set("n", "<leader>lco", builtin.lsp_outgoing_calls, {})
    end,
  },
  {
    "nvim-telescope/telescope-ui-select.nvim",
    config = function()
      require("telescope").setup({
        pickers = {
          find_files = {
            hidden = true,
          },
        },
        extensions = {
          ["ui-select"] = {
            require("telescope.themes").get_dropdown({}),
          },
        },
      })
      require("telescope").load_extension("ui-select")
    end,
  },
}
