import tkinter as tk
from tkinter import ttk

class Analytics_View:
  def __init__(self, root):
    self.__root = root
    self.__root.tk.call("source", "sun-valley.tcl")
    self._values = {
      'Colunas': ['Titulo', 'Publicacao', 'Canal', 'Trending', 'Views', 'Likes', 'Dislikes', 'Comentarios', 'Descricao', 'Categoria'],
      'Categorias': ['Education', 'Entertainment', 'Music', 'Science & Technology', 'People & Blogs', 'Gaming', 'Comedy', 'Film & Animation', 'Sports', 'News & Politics', 'Howto & Style', 'Travel & Events', 'Autos & Vehicles', 'Pets & Animals', 'Nonprofits & Activism'],
      'TipoGrafico': [
        'Barras: Top (n) Views', 
        'Barras: Top (n) Comentarios',
        'Barras: Top (n) Likes',
        'Dispersão: Views e Comentários',
        'Dispersão: Views e Likes',
        'Dispersão: Comentários e Likes',
        ]
    }
    self._selecao_combobox = {}
    self._treeview = None
    self._stringVars = {}
    self._labels = {}
    self._inputs = {}
    self._comboboxes = {}
    self._botoes = {}
    self._frames = {}

    self._create()
    self._tema()
    self._load()

  def insertDataTreeView(self, data):
    cont = 0
    for d in data:
      if cont % 2 == 0:
        self._treeview.insert('', tk.END, values=[d.titulo, d.dt_publicacao, d.canal, d.dt_trending, d.cont_views, d.likes, d.dislikes, d.cont_comentarios, d.descricao, d.categoria], tags = ('odd',))
      else:
        self._treeview.insert('', tk.END, values=[d.titulo, d.dt_publicacao, d.canal, d.dt_trending, d.cont_views, d.likes, d.dislikes, d.cont_comentarios, d.descricao, d.categoria], tags = ('even',))
  
  def habilitar_inputs(self):
    for elemento in self._labels:
      if elemento != 'QuantidadeN':
        self._labels[elemento].config(state=tk.NORMAL)
    for elemento in self._inputs:
      if elemento != 'QuantidadeN':
        self._inputs[elemento].config(state=tk.NORMAL)
    for elemento in self._comboboxes:
      self._comboboxes[elemento].config(state=tk.NORMAL)
    
    self._botoes['Limpar'].config(state=tk.NORMAL)
    self._botoes['Plotar'].config(state=tk.NORMAL)

  def _create(self):
    self._frames['Filtros'] = tk.Frame(self.__root)
    self._frames['Grafico'] = tk.LabelFrame(self.__root, text=f'Plotar Grafico')
    
    self._frames['Botoes'] = tk.Frame(self.__root, border=0)
    self._frames['Treeview'] = tk.Frame(self.__root, border=0)
    
    for frame in [ 'Periodo', 'Titulo', 'Categoria']:
      self._frames[frame] = tk.LabelFrame(self._frames['Filtros'], text=f'Filtrar por {frame}')
    
    self._labels['TipoGrafico'] = tk.Label(self._frames['Grafico'], text=f'Tipo do Grafico:', border=0, borderwidth=0, highlightthickness=0)
    self._labels['QuantidadeN'] = tk.Label(self._frames['Grafico'], text=f'Quantidade de Dados (n):', border=0, borderwidth=0, highlightthickness=0)

    self._labels['Inicio'] = tk.Label(self._frames['Periodo'], text=f'Data Inicial:', border=0, borderwidth=0, highlightthickness=0)
    self._labels['Fim'] = tk.Label(self._frames['Periodo'], text=f'Data Final:  ', border=0, borderwidth=0, highlightthickness=0)
    self._labels['Video'] = tk.Label(self._frames['Titulo'], text=f'Video: ', border=0, borderwidth=0, highlightthickness=0)
    self._labels['Canal'] = tk.Label(self._frames['Titulo'], text=f'Canal: ', border=0, borderwidth=0, highlightthickness=0)
    self._labels['Categoria'] = tk.Label(self._frames['Categoria'], text=f'Categoria: ', border=0, borderwidth=0, highlightthickness=0)
    
    for input in ['Video', 'Canal']:
      self._stringVars[input] = tk.StringVar()
      self._inputs[input] = tk.Entry(self._frames['Titulo'], textvariable=self._stringVars[input], border=0, borderwidth=0, highlightthickness=0)
    
    self._stringVars['Inicio'] = tk.StringVar()
    self._inputs['Inicio'] = tk.Entry(self._frames['Periodo'], textvariable=self._stringVars['Inicio'], border=0, borderwidth=0, highlightthickness=0)
    self._stringVars['Fim'] = tk.StringVar()
    self._inputs['Fim'] = tk.Entry(self._frames['Periodo'], textvariable=self._stringVars['Fim'], border=0, borderwidth=0, highlightthickness=0)

    self._stringVars['QuantidadeN'] = tk.StringVar()
    self._inputs['QuantidadeN'] = tk.Entry(self._frames['Grafico'], textvariable=self._stringVars['QuantidadeN'], border=0, borderwidth=0, highlightthickness=0)

    self._selecao_combobox['Categoria'] = tk.StringVar()
    self._comboboxes['Categoria'] = ttk.Combobox(self._frames['Categoria'], textvariable=self._selecao_combobox['Categoria'] , state='readonly', values=self._values['Categorias'])

    self._selecao_combobox['TipoGrafico'] = tk.StringVar()
    self._comboboxes['TipoGrafico'] = ttk.Combobox(self._frames['Grafico'], textvariable=self._selecao_combobox['TipoGrafico'] , state='readonly', values=self._values['TipoGrafico'])

    self._botoes['Arquivo'] = tk.Button(self._frames['Botoes'], text='Selecionar Arquivo', borderwidth=.5, highlightthickness=0, cursor="hand1")
    self._botoes['Limpar'] = tk.Button(self._frames['Botoes'], text='Limpar Filtro', borderwidth=.5, highlightthickness=0, cursor="hand1")
    self._botoes['Plotar'] = tk.Button(self._frames['Botoes'], text='Plotar Grafico', borderwidth=.5, highlightthickness=0, cursor="hand1")
    self._treeview = ttk.Treeview(self.__root, columns=self._values['Colunas'], show='headings')
    self._configure_treeview()
  
  def _load(self):
    self._frames['Filtros'].grid(row=0, column=0, sticky=tk.E+tk.W, pady=(5, 0), padx=(20, 0))

    self._frames['Titulo'].grid(row=0, column=0, sticky=tk.E+tk.W, pady=(5, 0), padx=(0, 10))
    self._labels['Video'].grid(row=0, column=0, sticky=tk.W+tk.S, pady=(10, 0), padx=(10, 0))
    self._inputs['Video'].grid(row=1, column=0, pady=(2, 15), padx=(5, 0), ipady=5)
    self._labels['Canal'].grid(row=0, column=1, sticky=tk.W+tk.S, pady=(10, 0), padx=(10, 0))
    self._inputs['Canal'].grid(row=1, column=1, pady=(2, 15), padx=(5, 10), ipady=5)

    self._frames['Periodo'].grid(row=0, column=1, sticky=tk.E+tk.W, pady=(5, 0), padx=(0, 10))
    self._labels['Inicio'].grid(row=0, column=1, pady=(3, 2), padx=(5, 0))
    self._inputs['Inicio'].grid(row=1, column=1, pady=(2, 15), padx=(5, 0), ipady=5)
    self._labels['Fim'].grid(row=0, column=2, pady=(3, 2), padx=(5, 0))
    self._inputs['Fim'].grid(row=1, column=2, pady=(2, 15), padx=(5, 10), ipady=5)

    self._frames['Categoria'].grid(row=0, column=2, sticky=tk.E+tk.W, pady=(5, 0), padx=(0, 5))
    self._labels['Categoria'].grid(row=0, column=0, sticky=tk.W+tk.S, pady=(5, 0), padx=(10, 0))
    self._comboboxes['Categoria'].grid(row=1, column=0, pady=(2, 10), sticky=tk.W+tk.S, padx=(10, 10))

    self._frames['Grafico'].grid(row=1, column=0, sticky=tk.E+tk.W, pady=(5, 0), padx=(20, 10))
    self._labels['TipoGrafico'].grid(row=0, column=0, pady=(2, 2), padx=(5, 0))
    self._comboboxes['TipoGrafico'].grid(row=1, column=0, pady=(2, 10), sticky=tk.W+tk.S, padx=(5,5))
    self._labels['QuantidadeN'].grid(row=0, column=1, pady=(2, 2), padx=(5, 0))
    self._inputs['QuantidadeN'].grid(row=1, column=1, pady=(5, 11), padx=(5, 5), ipady=5)

    self._frames['Botoes'].grid(row=2, column=0, sticky=tk.E, pady=(5, 0), padx=(0, 10))
    self._botoes['Arquivo'].grid(row=0, column=0, sticky=tk.W+tk.S, pady=(5, 0), padx=(10, 0))
    self._botoes['Limpar'].grid(row=0, column=1, sticky=tk.W+tk.S, pady=(5, 0), padx=(10, 0))
    self._botoes['Plotar'].grid(row=0, column=2, sticky=tk.W+tk.S, pady=(5, 0), padx=(10, 0))
    
    self._frames['Treeview'].grid(row=4, column=0, sticky=tk.E+tk.W, pady=(5, 0), padx=(0, 10))
    self._treeview.grid(row=4, column=0,columnspan=2, padx=(10, 10), pady=(10, 10))
    
    self._sb_y.grid(row=4, column=2, sticky='ns')
    self._sb_x.grid(row=5, column=0, columnspan=2, sticky='we')

    label = tk.Label(self.__root, text='Autor: Ernane Ferreira', border=0, borderwidth=0, highlightthickness=0)
    label.grid(row=6, column=0)

    for elemento in self._labels:
      self._labels[elemento].config(state=tk.DISABLED)
    for elemento in self._inputs:
      self._inputs[elemento].config(state=tk.DISABLED)
    for elemento in self._comboboxes:
      self._comboboxes[elemento].config(state=tk.DISABLED)
    
    self._botoes['Limpar'].config(state=tk.DISABLED)
    self._botoes['Plotar'].config(state=tk.DISABLED)
  
  def _configure_treeview(self):
    for col in self._values['Colunas']:
      self._treeview.heading(col, text=col)
      self._treeview.column(col, width=90, minwidth=100)

    self._sb_y = ttk.Scrollbar(self.__root, orient=tk.VERTICAL, command=self._treeview.yview)
    self._treeview.configure(yscroll=self._sb_y.set)

    self._sb_x = ttk.Scrollbar(self.__root, orient=tk.HORIZONTAL, command=self._treeview.xview)
    self._treeview.configure(xscroll=self._sb_x.set)
    
    self._treeview.grid(row=0, column=0)
    self._sb_y.grid(row=0, column=1, sticky='ns')
    self._sb_x.grid(row=1, column=0, sticky='we')

  def _tema(self):
    self.__root.tk.call("set_theme", "light")

    for el in self._inputs:
      self._inputs[el]['background'] = '#e6e5e5'

    self._treeview.tag_configure('odd', background='#E8E8E8')
    self._treeview.tag_configure('even', background='#DFDFDF')
      
      

if __name__ == "__main__":
  root = tk.Tk()
  root.title('Teste View')
  c = Analytics_View(root)
  tk.mainloop()