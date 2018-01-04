set hlsearch
set incsearch
set backspace=eol,start,indent
set whichwrap+=<,>,h,l
set ignorecase
set autoindent
set autoread
set ruler
set showmode
set nu

set history=700

filetype plugin on
filetype indent on

syntax enable
colorscheme desert
set background=dark

set so=7
set wildmenu
set wildignore=*.o,*~,*.pyc
set cmdheight=2
set hid
set smartcase
set lazyredraw
set magic
set showmatch
set mat=2
set noerrorbells
set novisualbell
set t_vb=
set tm=500

if has("gui_running")
	set guioptions-=T
	set guioptions+=e
	set t_Co=256
	set guitablabel=%M\ %t
endif

set fileencodings=utf8,gb2312,gb18030,gbk,ucs-bom,cp936,latin1
set ffs=unix,dos,mac

set nobackup
set nowb
set noswapfile

set smartindent
"set smarttab
set tabstop=4
set softtabstop=4
set shiftwidth=4
set expandtab
set list
set listchars=tab:>-,trail:-

set lbr
set tw=500

set ai
set si
set wrap


set viminfo^=%
set laststatus=2


