vim.cmd("set expandtab")
vim.cmd("set tabstop=2")
vim.cmd("set softtabstop=2")
vim.cmd("set shiftwidth=2")
vim.cmd("set number")
vim.cmd("set relativenumber")
vim.g.mapleader = " "

--Buffers
vim.keymap.set("n", "H", ":bnext<CR>", { desc = "Next buffer" })
vim.keymap.set("n", "L", ":bprevious<CR>", { desc = "Previous buffer" })
vim.keymap.set("n", "<leader>bq", ":bp<bar>sp<bar>bn<bar>bd<CR>", { desc = "Close the current buffer" })

-- Split Windows
vim.keymap.set("n", "<leader>wsh", ":split<CR>") -- Horizontal Split
vim.keymap.set("n", "<leader>wsv", ":vsplit<CR>") -- Vertical Split

-- Move Between Windows
vim.keymap.set("n", "<leader>wh", ":wincmd h<CR>") -- Move Left
vim.keymap.set("n", "<leader>wj", ":wincmd j<CR>") -- Move Down
vim.keymap.set("n", "<leader>wk", ":wincmd k<CR>") -- Move Up
vim.keymap.set("n", "<leader>wl", ":wincmd l<CR>") -- Move Right

-- Resize Windows
vim.keymap.set("n", "<leader>w<", ":resize -5<CR>") -- Resize Left
vim.keymap.set("n", "<leader>w>", ":resize +5<CR>") -- Resize Right
vim.keymap.set("n", "<leader>w+", ":vertical resize +5<CR>") -- Resize Up
vim.keymap.set("n", "<leader>w-", ":vertical resize -5<CR>") -- Resize Down

-- Close Windows
vim.keymap.set("n", "<leader>wq", ":close<CR>") -- Close Current Window
vim.keymap.set("n", "<leader>wa", ":only<CR>") -- Close All Except Current

-- Switch Between Windows
vim.keymap.set("n", "<leader>wp", ":wincmd w<CR>") -- Switch Last Used Window

-- Project
vim.keymap.set("n", "<leader>qq", ":qa<CR>") -- Quit all buffers
vim.keymap.set("n", "<leader>qf", ":qa!<CR>") -- Force quit all buffers

vim.opt.clipboard = "unnamedplus" -- Sync with clipboard
