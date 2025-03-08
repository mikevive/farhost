local M = {}

-- Table to store file paths indexed by numbers
M.file_marks = {}

-- Function to store the current file path associated with a number
function M.mark_file(number)
    if number >= 1 and number <= 5 then
        -- Store the current file path associated with the number
        local file_path = vim.fn.expand("%:p")
        if file_path ~= "" then
            M.file_marks[number] = file_path
            vim.notify("File marked for number " .. number .. ": " .. file_path)
        else
            vim.notify("No file to mark", vim.log.levels.WARN)
        end
    else
        vim.notify("Invalid number. Please use a number between 1 and 5.", vim.log.levels.ERROR)
    end
end

-- Function to jump to the file associated with a number
function M.goto_file(number)
    local file_path = M.file_marks[number]
    if file_path then
        vim.cmd("edit " .. vim.fn.fnameescape(file_path))
    else
        vim.notify("No file marked for number " .. number, vim.log.levels.WARN)
    end
end

-- Set up key mappings
function M.setup()
    -- Map <leader>m1 through <leader>m5 to mark files
    for i = 1, 5 do
        vim.keymap.set("n", "<leader>m" .. i, function()
            M.mark_file(i)
        end, { desc = "Mark file for " .. i })
    end

    -- Map <leader>1 through <leader>5 to go to the marked files
    for i = 1, 5 do
        vim.keymap.set("n", "<leader>" .. i, function()
            M.goto_file(i)
        end, { desc = "Go to file marked for " .. i })
    end
end

return M

