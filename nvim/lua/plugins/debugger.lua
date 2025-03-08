return {
  {
    "mfussenegger/nvim-dap",
    dependencies = {
      "rcarriga/nvim-dap-ui",
      "nvim-neotest/nvim-nio",
    },
    config = function()
      local dap = require("dap")
      local dapui = require("dapui")

      dapui.setup({
        layouts = {
          {
            elements = {
              -- These windows will only be displayed if they have content
              --{ id = "scopes",      size = 0.25 },
              { id = "breakpoints", size = 0.5 },
              --{ id = "stacks",      size = 0.25 },
              { id = "watches",     size = 0.5 },
            },
            size = 40,   -- Width of the window
            position = "left", -- Can be "left" or "right"
          },
          {
            elements = {
              { id = "repl",    size = 1 },
              --{ id = "console", size = 0.5 },
            },
            size = 10,     -- Height of the window
            position = "bottom", -- Can be "bottom" or "top"
          },
        },
        render = {
          max_type_length = nil, -- Adjust for better visibility
          show_unused = false, -- Hides unused elements
        },
      })

      dap.listeners.before.attach.dapui_config = function()
        dapui.open()
      end
      dap.listeners.before.launch.dapui_config = function()
        dapui.open()
      end
      dap.listeners.before.event_terminated.dapui_config = function()
        dapui.close()
      end
      dap.listeners.before.event_exited.dapui_config = function()
        dapui.close()
      end

      vim.keymap.set("n", "<Leader>db", ":DapToggleBreakpoint<CR>")
      vim.keymap.set("n", "<Leader>dc", ":DapContinue<CR>")
      vim.keymap.set("n", "<Leader>dq", ":DapTerminate<CR>")
      vim.keymap.set("n", "<Leader>ds", ":DapStepOver<CR>")
      vim.keymap.set("n", "<Leader>di", ":DapStepInto<CR>")
      vim.keymap.set("n", "<Leader>do", ":DapStepOut<CR>")

      local mason_path = vim.fn.stdpath("data") .. "/mason/packages/js-debug-adapter"

      dap.adapters["pwa-node"] = {
        type = "server",
        host = "localhost",
        port = "${port}",
        executable = {
          command = "node",
          args = { mason_path .. "/js-debug/src/dapDebugServer.js", "${port}" },
        },
      }
      for _, language in ipairs({ "typescript", "javascript" }) do
        dap.configurations[language] = {
          {
            type = "pwa-node",
            request = "launch",
            name = "Launch file",
            program = "${file}",
            cwd = "${workspaceFolder}",
          },
          {
            type = "pwa-node",
            request = "attach",
            name = "Attach",
            processId = require("dap.utils").pick_process,
            cwd = "${workspaceFolder}",
          },
        }
      end
    end,
  },
}
