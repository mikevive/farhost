return {
	{
		"nvim-telescope/telescope.nvim",
		tag = "0.1.6",
		dependencies = {
			"nvim-lua/plenary.nvim",

			-- fzf native extension
			{
				"nvim-telescope/telescope-fzf-native.nvim",
				build = "make",
				cond = vim.fn.executable("make") == 1,
			},

			-- ui-select extension
			{
				"nvim-telescope/telescope-ui-select.nvim",
			},

			-- live grep args extension
			{
				"nvim-telescope/telescope-live-grep-args.nvim",
			},
		},
		config = function()
			local telescope = require("telescope")
			local builtin = require("telescope.builtin")
			local lga = require("telescope").extensions.live_grep_args

			telescope.setup({
				defaults = {
					file_ignore_patterns = { "node_modules", "%.git/", "dist" },
					previewer = false,
					sorting_strategy = "ascending",
					layout_strategy = "horizontal",
					layout_config = {
						prompt_position = "top",
						height = 0.4,
						width = 0.6,
					},
					results_title = false,
					path_display = { "truncate" },
				},
				pickers = {
					find_files = {
						hidden = true,
						find_command = {
							"fd",
							"--type",
							"f",
							"--strip-cwd-prefix",
							"--hidden",
							"--exclude",
							"node_modules",
							"--exclude",
							".git",
							"--exclude",
							"dist",
						},
					},
				},
				extensions = {
					fzf = {
						fuzzy = true,
						override_generic_sorter = true,
						override_file_sorter = true,
						case_mode = "smart_case",
					},
					["ui-select"] = {
						require("telescope.themes").get_dropdown({}),
					},
					live_grep_args = {
						auto_quoting = true,
					},
				},
			})

			-- Load extensions
			telescope.load_extension("fzf")
			telescope.load_extension("ui-select")
			telescope.load_extension("live_grep_args")

			-- Keymaps
			vim.keymap.set("n", "<leader><space>", builtin.find_files, {})
			vim.keymap.set("n", "<leader>fg", lga.live_grep_args, {})
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
}
