return {
	"nvim-neo-tree/neo-tree.nvim",
	dependencies = {
		"nvim-lua/plenary.nvim",
		"nvim-tree/nvim-web-devicons",
		"MunifTanjim/nui.nvim",
	},
	config = function()
		local function file_renamed_handler(args)
			local changes = {
				files = {
					{
						oldUri = vim.uri_from_fname(args.source),
						newUri = vim.uri_from_fname(args.destination),
					},
				},
			}

			local clients = (vim.lsp.get_clients or vim.lsp.get_active_clients)()
			for _, client in ipairs(clients) do
				if client.supports_method("workspace/willRenameFiles") then
					local resp = client.request_sync("workspace/willRenameFiles", changes, 1000, 0)
					if resp and resp.result ~= nil then
						vim.lsp.util.apply_workspace_edit(resp.result, client.offset_encoding)
					end
				end
				if client.supports_method("workspace/didRenameFiles") then
					client.notify("workspace/didRenameFiles", changes)
				end
			end
		end

		require("neo-tree").setup({
			filesystem = {
				filtered_items = {
					visible = true,
					hide_dotfiles = false,
					hide_gitignored = true,
				},
			},
			window = {
				position = "float",
				popup = {
					size = { height = "100%", width = "100%" },
					position = "50%",
				},
			},
			event_handlers = {
				{ event = "file_renamed", handler = file_renamed_handler },
				{ event = "file_moved", handler = file_renamed_handler },
			},
		})
		vim.keymap.set("n", "<C-p>", ":Neotree toggle reveal<CR>", {})
	end,
}
