import warnings ; warnings.filterwarnings("ignore", category=FutureWarning) # Remove o `Warning` referente a futura remocao do datetime do Pandas.
import pandas as pd
import tkinter.messagebox as messagebox

class Video:
    def __init__(self, data):
        self.id_video = data[0]
        self.titulo = data[1]
        self.dt_publicacao = data[2]
        self.id_canal = data[3]
        self.canal = data[4]
        self.dt_trending = data[5]
        self.cont_views = data[6]
        self.likes = data[7]
        self.dislikes = data[8]
        self.cont_comentarios = data[9]
        self.descricao = data[10]
        self.categoria = data[11]
    
    def __str__(self):
        r = f"{self.canal}\n{self.titulo}\n{self.categoria}\nViews: {self.cont_views}\nComentarios: {self.cont_comentarios}\nLikes: {self.likes}\nPublicado em {self.dt_publicacao}\n----------------------------------------------"
        return r

class Analytics:            
  def lista_categorias(self):
    return list(self._dataframe.categoria.unique())

  def busca_por_titulo(self, titulo):
    filtro = self._dataframe.titulo.str.contains(titulo, case=False)
    for i, el in enumerate(filtro):
      if pd.isnull(float(el)):
        filtro[i] = False
    param = self._dataframe[filtro]

    return self._df_para_lista(param)

  def busca_por_canal(self, canal):
    filtro = self._dataframe.canal.str.contains(canal, case=False)
    for i, el in enumerate(filtro):
      if pd.isnull(float(el)):
        filtro[i] = False
    param = self._dataframe[filtro]

    return self._df_para_lista(param)

  def busca_por_categoria(self, categoria):
    filtro = self._dataframe.categoria.str.contains(categoria, case=False)
    for i, el in enumerate(filtro):
      if pd.isnull(float(el)):
        filtro[i] = False
    param = self._dataframe[filtro]

    return self._df_para_lista(param)

  def busca_por_periodo(self, ini, fim):
    return self._df_para_lista(self._dataframe[(self._dataframe.dt_publicacao.dt.date >= pd.to_datetime(ini)) & (self._dataframe.dt_publicacao.dt.date <= pd.to_datetime(fim))])

  def busca_todos(self):
    return self._df_para_lista(self._dataframe)

  def top(self, n, col):
    if int(n) < 1: 
      raise ValueError()
    else:
      return self._dataframe.sort_values(by=[col], ascending=False).head(int(n))

  def ordenar(self, tv, col, reverse):
    if tv.get_children('') != ():
      print("╔════════════════════════════════════════════════════════════════════════════════════════════════╗")
      print(f"                                    ORDENANDO POR {col.upper()}                                  ")
      print("╚════════════════════════════════════════════════════════════════════════════════════════════════╝")
      l = [(tv.set(k, col), k) for k in tv.get_children('')]
      l.sort(reverse=reverse)

      for index, (val, k) in enumerate(l):
          tv.move(k, '', index)

      tv.heading(col, command=lambda: self.ordenar(tv, col, not reverse))
    else:
      messagebox.showinfo(title="Sem dados", message="Voce precisa inserir dados para poder ordena-los.")
      print("╔════════════════════════════════════════════════════════════════════════════════════════════════╗")
      print(f"                                     SEM DADOS PARA ORDENAR                                      ")
      print("╚════════════════════════════════════════════════════════════════════════════════════════════════╝")
  
  def clear(self, treeview):
    treeview.delete(*treeview.get_children())
      
  def seleciona_arquivo(self, fd, root):
    tipos_arq = (('Arquivos .csv', '*.csv'), ('Todos os arquivos', '*.*'))
    
    arquivo = fd.askopenfilename(
      title='Abrir arquivo',
      filetypes=tipos_arq)
    title = ' '.join(arquivo.split('/')[len(arquivo.split('/'))-1].split('.')[0].split('_'))

    self._dataframe = pd.read_csv(arquivo, lineterminator='\n')
    
    self._dataframe.dt_publicacao = pd.to_datetime(self._dataframe.dt_publicacao)
    self._dataframe.dt_trending = pd.to_datetime(self._dataframe.dt_trending)
    
    print("╔════════════════════════════════════════════════════════════════════════════════════════════════╗")
    print("║                                   INFORMAÇÔES DO ARQUIVO                                       ║")
    print("╚════════════════════════════════════════════════════════════════════════════════════════════════╝")
    print("╔════════════════════════════════════════════════════════════════════════════════════════════════╗")
    print(f"║ ARQUIVO: {title}")  
    print("╠════════════════════════════════════════════════════════════════════════════════════════════════╣")      
    print("║ Possui dados dos vídeos em tendência no Youtube BR                                             ║")
    print("╠════════════════════════════════════════════════════════════════════════════════════════════════╣")
    print(f"║ TOTAL DE VIDEOS: {len(self._dataframe)}")  
    print("╠════════════════════════════════════════════════════════════════════════════════════════════════╣")      
    print(f"║ PERIODO: {self._dataframe.dt_publicacao.min()} até {self._dataframe.dt_publicacao.max()}")
    print("╠════════════════════════════════════════════════════════════════════════════════════════════════╣")
    print("║ DADOS DOS VIDEOS:")
    for c in self._dataframe.columns.to_list():
        print(f"║ {c}")
    print("╚════════════════════════════════════════════════════════════════════════════════════════════════╝")

    return title

  def _df_para_lista(self, df):
    data = [
      tup for tup in zip( 
        df.id_video, 
        df.titulo,
        df.dt_publicacao, 
        df.id_canal,
        df.canal, 
        df.dt_trending,
        df.cont_views, 
        df.likes,
        df.dislikes, 
        df.cont_comentarios,
        df.descricao, 
        df.categoria
      )
    ]
    videos = list()
    for tup in data:
      videos.append(Video(tup))
    return videos

if __name__ == '__main__':
    print('\n.::Base de Dados: ')
    path = f"{__file__.replace('models/Analytics.py','data/')}"
    print(f'../data/BR_youtube_trending_data_completo.csv')
    ld = Analytics(f'{path}BR_youtube_trending_data_completo.csv')
    print("\n\n.::Lista de Categorias: \n",ld.lista_categorias())
    
    res = ld.busca_por_titulo('fla')
    print('\n.::Busca por Titulo: ')
    for v in res:
        print(v)
        
    res = ld.busca_por_canal('espor')
    print('\n.::Busca por Canal: ')
    for v in res:
        print(v)
    
    
    res = ld.busca_por_categoria('SPORTS')
    print('\n.::Busca por Categoria: ')
    for v in res:
        print(v)
    
    res = ld.busca_por_periodo('2020-11-01', '2020-11-30')
    print('\n.::Busca por Periodo: ')
    for v in res:
        print(v)
    
    res = ld.busca_todos()
    print('\n.:: Todos os videos: ')
    for v in res:
        print(v)

    print("\n\n.::Lista de Categorias: \n",ld.lista_categorias())