let SessionLoad = 1
let s:so_save = &g:so | let s:siso_save = &g:siso | setg so=0 siso=0 | setl so=-1 siso=-1
let v:this_session=expand("<sfile>:p")
doautoall SessionLoadPre
let Lf_StlColorscheme = "everforest"
let VM_Insert_hl = "VMCursor"
let Lf_PopupColorscheme = "everforest"
let VM_Mono_hl = "VMCursor"
let VM_Cursor_hl = "VMCursor"
let VM_Extend_hl = "Visual"
silent only
silent tabonly
cd ~/Documents/api/project
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
let s:shortmess_save = &shortmess
set shortmess+=aoO
badd +10 ~/Documents/api/project/profile_api/views.py
badd +30 ~/Documents/api/project/profile_api/serializers.py
badd +16 ~/Documents/api/project/profile_api/urls.py
badd +1 ~/Documents/api/project/profile_api/permissions.py
badd +63 ~/Documents/api/project/profile_api/models.py
badd +6 ~/Documents/api/project/profile_api/admin.py
argglobal
%argdel
$argadd .
edit ~/Documents/api/project/profile_api/urls.py
wincmd t
let s:save_winminheight = &winminheight
let s:save_winminwidth = &winminwidth
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
argglobal
balt ~/Documents/api/project/profile_api/permissions.py
setlocal foldmethod=expr
setlocal foldexpr=v:lua.LazyVim.treesitter.foldexpr()
setlocal foldmarker={{{,}}}
setlocal foldignore=#
setlocal foldlevel=99
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldenable
11
sil! normal! zo
let s:l = 16 - ((15 * winheight(0) + 11) / 23)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 16
normal! 0
tabnext 1
if exists('s:wipebuf') && len(win_findbuf(s:wipebuf)) == 0 && getbufvar(s:wipebuf, '&buftype') isnot# 'terminal'
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20
let &shortmess = s:shortmess_save
let &winminheight = s:save_winminheight
let &winminwidth = s:save_winminwidth
let s:sx = expand("<sfile>:p:r")."x.vim"
if filereadable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &g:so = s:so_save | let &g:siso = s:siso_save
set hlsearch
nohlsearch
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
