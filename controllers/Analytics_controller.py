from datetime import datetime
import tkinter as tk
import numpy as np
import tkinter.filedialog as fd
import tkinter.messagebox as messagebox
import matplotlib.pyplot as plt
import seaborn as sns
import re

class Analytics_Controller():
  def __init__(self):
    self._root = tk.Tk()
    self._root.title('Analytics')
    
    self._model = None
    self._view = None
    self._temp_index = None
    self._key = tk.StringVar()

  def initialize(self, model, view):
    self._model = model
    self._view = view
    self._setsUp()

  def execute(self):
    self._root.mainloop()

  def creditos(self):
    print("\n\n╔════════════════════════════════════════════════════════════════════════════════════════════════╗")
    print("║                                     OBRIGADO POR UTILIZAR! :)                                  ║")  
    print("╚════════════════════════════════════════════════════════════════════════════════════════════════╝") 
    print("╠═════ ═════ ═════ ═════ ═════ ═════ ═════ ═════ ═════ ═════ ═════ ═════ ═════ ════ ═════ ═════ ═╣") 
    print("╔════════════════════════════════════════════════════════════════════════════════════════════════╗")
    print("║                                       INFORMAÇÔES UTEIS                                        ║")
    print("╚════════════════════════════════════════════════════════════════════════════════════════════════╝")    
    print("╔════════════════════════════════════════════════════════════════════════════════════════════════╗")
    print("║                                             PROJETO                                            ║")
    print("╠════════════════════════════════════════════════════════════════════════════════════════════════╣")
    print("║ Sistema desenvolvido como projeto final da materia de Programacao Orientada a Objeto (POO) com ║")
    print("║ a liguagem Python no semestre de 2021.1 na Escola de Ciencias e Tecnologia da Universidade     ║")
    print("║ Federal do Rio Grande do Norte (ECT/UFRN).                                                     ║")
    print("╚════════════════════════════════════════════════════════════════════════════════════════════════╝")
    print("╔════════════════════════════════════════════════════════════════════════════════════════════════╗")
    print("║                                             AUTOR                                              ║")  
    print("╠════════════════════════════════════════════════════════════════════════════════════════════════╣")      
    print("║ Ernane Ferreira                                                                                ║")
    print("║ Github: https://github.com/ErnaneJ                                                             ║")
    print("║ Outras Redes: https://ernanej.github.io/my-linktree/                                           ║")
    print("╚════════════════════════════════════════════════════════════════════════════════════════════════╝")
    print("╔════════════════════════════════════════════════════════════════════════════════════════════════╗")
    print("║                                           CODIGO FONTE                                         ║")  
    print("╠════════════════════════════════════════════════════════════════════════════════════════════════╣")      
    print("║ Código fonte disponível em:                                                                    ║")
    print("║ https://github.com/ErnaneJ/youtube-analytics                                                   ║")
    print("╚════════════════════════════════════════════════════════════════════════════════════════════════╝")
  
  @property
  def root(self):
    return self._root

  def _setsUp(self):
    self._root.bind('<Any-KeyPress>', self._keypress)

    self._view._botoes['Arquivo']['command'] = lambda: self._processa_selecao()
    self._view._botoes['Limpar']['command'] = lambda: self._limpa_filtros()
    self._view._botoes['Plotar']['command'] = lambda: self._plotar_grafico()

    self._view._stringVars['Video'].trace('w', lambda nm, idx, mode, var=self._view._stringVars['Video']:self._processa_busca('Video', self._view._stringVars['Video']))
    self._view._stringVars['Canal'].trace('w', lambda nm, idx, mode, var=self._view._stringVars['Canal']:self._processa_busca('Canal', self._view._stringVars['Canal']))
    self._view._stringVars['Inicio'].trace('w', lambda nm, idx, mode, var=self._view._stringVars['Inicio']:self._processa_busca('Inicio'))
    self._view._stringVars['Fim'].trace('w', lambda nm, idx, mode, var=self._view._stringVars['Fim']:self._processa_busca('Fim'))

    self._view._comboboxes['TipoGrafico'].bind('<<ComboboxSelected>>', self._define_tipo_grafico)
    self._view._comboboxes['Categoria'].bind('<<ComboboxSelected>>', self._processa_categoria)
    
    self._view._treeview.heading('Titulo', text='Titulo', command=lambda: self._model.ordenar(self._view._treeview, 'Titulo', False))
    self._view._treeview.heading('Publicacao', text='Publicacao', command=lambda: self._model.ordenar(self._view._treeview, 'Publicacao', False))
    self._view._treeview.heading('Canal', text='Canal', command=lambda: self._model.ordenar(self._view._treeview, 'Canal', False))
    self._view._treeview.heading('Trending', text='Trending', command=lambda: self._model.ordenar(self._view._treeview, 'Trending', False))
    self._view._treeview.heading('Views', text='Views', command=lambda: self._model.ordenar(self._view._treeview, 'Views', False))
    self._view._treeview.heading('Likes', text='Likes', command=lambda: self._model.ordenar(self._view._treeview, 'Likes', False))
    self._view._treeview.heading('Dislikes', text='Dislikes', command=lambda: self._model.ordenar(self._view._treeview, 'Dislikes', False))
    self._view._treeview.heading('Comentarios', text='Comentarios', command=lambda: self._model.ordenar(self._view._treeview, 'Comentarios', False))
    self._view._treeview.heading('Descricao', text='Descricao', command=lambda: self._model.ordenar(self._view._treeview, 'Descricao', False))
    self._view._treeview.heading('Categoria', text='Categoria', command=lambda: self._model.ordenar(self._view._treeview, 'Categoria', False))

  def _define_tipo_grafico(self, event):
    tipo = self._view._selecao_combobox['TipoGrafico'].get()
    if 'Barras' in tipo:
      self._view._labels['QuantidadeN'].config(state=tk.NORMAL)
      self._view._inputs['QuantidadeN'].config(state=tk.NORMAL)
    elif 'Dispersão' in tipo:
      self._view._inputs['QuantidadeN'].config(state=tk.DISABLED)
      self._view._labels['QuantidadeN'].config(state=tk.DISABLED)

  def _plotar_grafico(self):
    tipo = self._view._selecao_combobox['TipoGrafico'].get()
    n = self._view._inputs['QuantidadeN'].get()
    ylabel =  ''
    xlabel = ''
    plot = True

    if 'Views' in tipo and 'Barras' in tipo:
      ylabel =  'Views'
      xlabel = 'Video'
      try: 
        data = self._model.top(n,'cont_views') 
        sns.catplot(data=data, x='titulo', y='cont_views', kind='bar',ci=None, legend_out=False, aspect=2)
        plt.xticks(rotation=90)
      except:
        plot = False
        messagebox.showwarning(title='Valor Invalido', message='\'n\' nao e um valor valido ou nao foi atribuido.')
    elif 'Comentarios' in tipo and 'Barras' in tipo:
      ylabel =  'Comentarios'
      xlabel = 'Video'
      try: 
        data = self._model.top(n,'cont_comentarios') 
        sns.catplot(data=data, x='titulo', y='cont_comentarios', kind='bar',ci=None, legend_out=False, aspect=2)
        plt.xticks(rotation=90)
      except:
        plot = False
        messagebox.showwarning(title='Valor Invalido', message='\'n\' nao e um valor valido ou nao foi atribuido.')
    elif 'Likes' in tipo and 'Barras' in tipo:
      ylabel =  'Likes'
      xlabel = 'Video'
      try: 
        data = self._model.top(n,'likes') 
        sns.catplot(data=data, x='titulo', y='likes', kind='bar',ci=None, legend_out=False, aspect=2)
        plt.xticks(rotation=90)
      except:
        plot = False
        messagebox.showwarning(title='Valor Invalido', message='\'n\' nao e um valor valido ou nao foi atribuido.') 
    elif 'Views e Comentários' in tipo and 'Dispersão' in tipo:
      ylabel =  'Views'
      xlabel = 'Comentários'
      sns.scatterplot(data=self._model._dataframe, x='cont_views', y='cont_comentarios')
      plt.yticks(np.arange(0, self._model._dataframe.cont_comentarios.max() + 10, step=400000))
      plt.xticks(np.arange(0, self._model._dataframe.cont_views.max(), step=2000000)) #fazer com que step seja 10% do maximo
      plt.grid()
      plt.ticklabel_format(style='plain', axis='x')
    elif 'Views e Likes' in tipo and 'Dispersão' in tipo:
      ylabel =  'Views'
      xlabel = 'Likes'
      sns.scatterplot(data=self._model._dataframe, x='cont_views', y='likes')
      plt.yticks(np.arange(0, self._model._dataframe.cont_views.max() + 10, step=400000))
      plt.xticks(np.arange(0, self._model._dataframe.likes.max(), step=2000000))
      plt.grid()
      plt.ticklabel_format(style='plain', axis='x')
    elif 'Comentários e Likes' in tipo and 'Dispersão' in tipo:
      ylabel = 'Comentários'
      xlabel = 'Likes'
      sns.scatterplot(data=self._model._dataframe, x='cont_comentarios', y='likes')
      plt.yticks(np.arange(0, self._model._dataframe.cont_comentarios.max() + 10, step=400000))
      plt.xticks(np.arange(0, self._model._dataframe.likes.max(), step=2000000))
      plt.grid()
      plt.ticklabel_format(style='plain', axis='x')

    if plot : 
      plt.ylabel(ylabel)
      plt.xlabel(xlabel)
      plt.ticklabel_format(style='plain', axis='y')
      
      plt.tight_layout()
      plt.show()
      self._view._selecao_combobox['TipoGrafico'].set('')
      self._view._inputs['QuantidadeN'].delete(0, 'end')
      self._view._inputs['QuantidadeN'].config(state=tk.DISABLED)
      self._view._labels['QuantidadeN'].config(state=tk.DISABLED)

  def _processa_categoria(self, event):
    categoria = self._view._selecao_combobox['Categoria'].get()
    self._view._inputs['Video'].config(state=tk.DISABLED)
    self._view._labels['Video'].config(state=tk.DISABLED)
    self._view._inputs['Canal'].config(state=tk.DISABLED)
    self._view._labels['Canal'].config(state=tk.DISABLED)
    self._view._inputs['Inicio'].config(state=tk.DISABLED)
    self._view._labels['Inicio'].config(state=tk.DISABLED)
    self._view._inputs['Fim'].config(state=tk.DISABLED)
    self._view._labels['Fim'].config(state=tk.DISABLED)
    self._model.clear(self._view._treeview)
    self._view.insertDataTreeView(self._model.busca_por_categoria(categoria))

  def _processa_selecao(self):
    try:
      self._root.title(f'Analytics - {self._model.seleciona_arquivo(fd, self._root)}')
      self._model.clear(self._view._treeview)
      self._view.insertDataTreeView(self._model.busca_todos())
      self._view.habilitar_inputs()
    except:
      print("╔════════════════════════════════════════════════════════════════════════════════════════════════╗")
      print(f"                                     NENHUM ARQUIVO FOI SELECIIONADO                             ")
      print("╚════════════════════════════════════════════════════════════════════════════════════════════════╝")
  
  def _limpa_filtros(self):
    self._model.clear(self._view._treeview)
    self._view._inputs['Video'].delete(0, 'end')
    self._view._inputs['Video'].config(state=tk.NORMAL)
    self._view._labels['Video'].config(state=tk.NORMAL)

    self._view._inputs['Canal'].delete(0, 'end')
    self._view._inputs['Canal'].config(state=tk.NORMAL)
    self._view._labels['Canal'].config(state=tk.NORMAL)

    self._view._inputs['Inicio'].delete(0, 'end')
    self._view._inputs['Inicio'].config(state=tk.NORMAL)
    self._view._labels['Inicio'].config(state=tk.NORMAL)

    self._view._inputs['Fim'].delete(0, 'end')
    self._view._inputs['Fim'].config(state=tk.NORMAL)
    self._view._labels['Fim'].config(state=tk.NORMAL)

    self._view._selecao_combobox['Categoria'].set('')
    self._view._comboboxes['Categoria'].config(state=tk.NORMAL)
    self._view._labels['Categoria'].config(state=tk.NORMAL)

    self._view.insertDataTreeView(self._model.busca_todos())

  def _processa_busca(self, tipo, stringVar = None):
    self._model.clear(self._view._treeview)
    if tipo == 'Video':
      self._view.insertDataTreeView(self._model.busca_por_titulo(stringVar.get()))
      self._view._inputs['Canal'].config(state=tk.DISABLED)
      self._view._inputs['Inicio'].config(state=tk.DISABLED)
      self._view._inputs['Fim'].config(state=tk.DISABLED)
      self._view._comboboxes['Categoria'].config(state=tk.DISABLED)
      self._view._labels['Canal'].config(state=tk.DISABLED)
      self._view._labels['Inicio'].config(state=tk.DISABLED)
      self._view._labels['Fim'].config(state=tk.DISABLED)
      self._view._labels['Categoria'].config(state=tk.DISABLED)
      if stringVar.get() == "" : self._limpa_filtros()
    elif tipo == 'Canal':
      self._view.insertDataTreeView(self._model.busca_por_canal(stringVar.get()))
      self._view._inputs['Video'].config(state=tk.DISABLED)
      self._view._inputs['Inicio'].config(state=tk.DISABLED)
      self._view._inputs['Fim'].config(state=tk.DISABLED)
      self._view._comboboxes['Categoria'].config(state=tk.DISABLED)
      self._view._labels['Video'].config(state=tk.DISABLED)
      self._view._labels['Inicio'].config(state=tk.DISABLED)
      self._view._labels['Fim'].config(state=tk.DISABLED)
      self._view._labels['Categoria'].config(state=tk.DISABLED)
      if stringVar.get() == "" : self._limpa_filtros()
    elif tipo == 'Inicio' or tipo == 'Fim': 
      self._format(tipo)
      if self._validaData():
        self._model.clear(self._view._treeview)
        self._view.insertDataTreeView(self._model.busca_por_periodo(self._view._stringVars['Inicio'].get(), self._view._stringVars['Fim'].get()))
        self._view._inputs['Video'].config(state=tk.DISABLED)
        self._view._inputs['Canal'].config(state=tk.DISABLED)
        self._view._comboboxes['Categoria'].config(state=tk.DISABLED)
        self._view._labels['Video'].config(state=tk.DISABLED)
        self._view._labels['Canal'].config(state=tk.DISABLED)
        self._view._labels['Categoria'].config(state=tk.DISABLED)
      else: self._view.insertDataTreeView(self._model.busca_todos())
      if (self._view._stringVars['Inicio'].get() == "" and self._view._stringVars['Fim'].get() == "") : self._limpa_filtros()
  
  def _format(self, input):
    self._view._stringVars[input].set(re.sub('[^0-9|-]','',self._view._stringVars[input].get()))
    if self._key.get() != 'BackSpace':
      if  len(self._view._stringVars[input].get()) > 10: self._view._stringVars[input].set(self._view._stringVars[input].get()[:-1])
      
      txt = ''.join(self._view._stringVars[input].get().split('-'))
      self._view._stringVars[input].set('')
      self._view._stringVars[input].set('{}-{}-{}'.format(txt[:4], txt[4:6], txt[6:8]))
      
      if txt == '' : self._view._stringVars[input].set(txt)
      self._view._inputs[input].icursor(self._view._inputs[input].index(tk.END))
        
  def _validaData(self):
    dataI = self._view._stringVars['Inicio'].get()
    dataF = self._view._stringVars['Fim'].get()

    if len(dataI)<10 or len(dataF)<10: return False

    try:
      anoI, mesI, diaI = dataI.split('-')
      anoF, mesF, diaF = dataF.split('-')
      return True
    except:
      messagebox.showwarning(title='Data Invalida', message='O conjunto de datas inserido nao e valido.')
      print("╔════════════════════════════════════════════════════════════════════════════════════════════════╗")
      print("║                                       DATA INVALIDA                                            ║")
      print("╚════════════════════════════════════════════════════════════════════════════════════════════════╝")
      return False
  
  def _keypress(self, event = None): 
    self._key.set(event.keysym)
