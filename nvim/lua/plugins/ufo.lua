return {
  "kevinhwang91/nvim-ufo",
  dependencies = "kevinhwang91/promise-async",
  event = "UIEnter", -- needed for folds to load in time and comments being closed
  init = function()
    vim.o.foldcolumn = "1"
    vim.o.foldlevel = 99
    vim.o.foldlevelstart = 99
    vim.o.foldenable = true
  end,
  config = function()
    local capabilities = vim.lsp.protocol.make_client_capabilities()
    capabilities.textDocument.foldingRange = {
      dynamicRegistration = false,
      lineFoldingOnly = true,
    }

    local clients = (vim.lsp.get_clients or vim.lsp.get_active_clients)()
    for _, client in ipairs(clients) do
      require("lspconfig")[client].setup({
        capabilities = capabilities,
      })
    end

    local ufo = require("ufo")
    vim.keymap.set("n", "zO", ufo.openAllFolds)
    vim.keymap.set("n", "zC", ufo.closeAllFolds)
    ufo.setup()
  end,
}
