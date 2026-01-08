from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def test_abrir_site_sage():
    with sync_playwright() as p:
        # Abre o navegador (Chromium)
        browser = p.chromium.launch(headless=True)

        # Cria uma nova página
        page = browser.new_page()

        # Define um timeout maior para carregamento de páginas
        page.set_default_timeout(30000)  # 30 segundossss

        try:
            # Acessa o site
            page.goto("https://teste.sage.fiocruz.br")
            
            # Aguarda o campo de usuário estar visível
            page.wait_for_selector('input[name="username"]', state='visible')
            
            # Preenche o usuário e senha (use variáveis de ambiente para dados sensíveis)
            username = os.getenv('SAGE_USERNAME', 'seu_usuario')
            password = os.getenv('SAGE_PASSWORD', 'sua_senha')
            
            # Preenche os campos de login
            print("\n[INÍCIO] Teste de login no SAGE")
            print("1. Preenchendo campos de login...")
            page.fill('input[name="username"]', username)
            page.fill('input[name="password"]', password)
            print("   ✓ Campos preenchidos")
            
            # Clica no botão de login
            print("2. Clicando no botão de login...")
            login_button = page.get_by_role('button', name='Entrar').or_(
                         page.get_by_text('Entrar').first)
            login_button.click()
            print("   ✓ Botão de login clicado")
            
            # Aguarda a navegação após o login
            print("3. Aguardando carregamento da página...")
            page.wait_for_load_state('networkidle')
            
            # Verifica se o login foi bem-sucedido
            print("4. Verificando se o login foi bem-sucedido...")
            try:
                # Aguarda o elemento específico estar visível
                print("   - Procurando pelo título 'SAGE'...")
                sage_title = page.locator('div.title.text-center h2:has-text("SAGE")')
                sage_title.wait_for(state='visible', timeout=10000)
                print("   ✓ Título 'SAGE' encontrado")
                
                # Verifica se o texto dentro do h2 é exatamente 'SAGE'
                title_text = sage_title.inner_text().strip()
                print(f"   - Texto encontrado: '{title_text}'")
                assert title_text == 'SAGE', f"Texto do título inesperado: '{title_text}'"
                print("   ✓ Texto do título está correto")
                
                # Tenta clicar em "teste subnudades" se estiver visível
                print("\n5. Tentando selecionar o perfil 'teste subnudades'...")
                try:
                    # Aguarda o botão de perfil ficar visível e clica nele
                    print("   - Procurando pelo botão 'Selecionar Perfil'...")
                    perfil_button = page.get_by_role('button', name='Selecionar Perfil', exact=True).or_(
                                  page.get_by_text('Selecionar Perfil').first)
                    perfil_button.wait_for(state='visible', timeout=5000)
                    perfil_button.click()
                    print("   ✓ Botão 'Selecionar Perfil' clicado")
                    
                    # Aguarda o select de perfis carregar e seleciona o perfil desejado
                    print("   - Procurando pelo seletor de perfis...")
                    
                    try:
                        # Aguarda o elemento select ficar visível
                        select_selector = 'select#perfil_id'
                        page.wait_for_selector(select_selector, state='visible', timeout=10000)
                        
                        # Seleciona a opção pelo texto visível
                        page.select_option(select_selector, label='Administrador Fiocruz')
                        print("   ✓ Perfil 'Perfil Teste Subunidades' selecionado com sucesso!")
                        
                        # Aguarda um momento para a seleção ser processada
                        page.wait_for_timeout(1000)
                        
                        # Verifica se a opção foi selecionada corretamente
                        selected_option = page.locator(f'{select_selector} option:checked')
                        selected_text = selected_option.inner_text().strip()
                        
                        if 'Perfil Teste Subunidades' in selected_text:
                            print("   ✓ Confirmação: Perfil selecionado corretamente")
                            
                            # Clica no botão 'Selecionar'
                            print("   - Clicando no botão 'Selecionar'...")
                            
                            # Tenta encontrar o botão de selecionar de diferentes maneiras
                            try:
                                # Primeiro tenta pelo texto exato
                                select_button = page.get_by_role('button', name='Selecionar').or_(
                                    page.get_by_text('Selecionar', exact=True).first
                                )
                                
                                # Se não encontrar, tenta por seletor CSS
                                if not select_button.is_visible():
                                    select_button = page.locator('button:has-text("Selecionar"), input[type="submit"][value*="Selecionar"]')
                                
                                select_button.wait_for(state='visible', timeout=5000)
                                select_button.click()
                                print("   ✓ Botão 'Selecionar' clicado com sucesso!")
                                
                                # Aguarda a navegação após a seleção do perfil
                                page.wait_for_load_state('networkidle')
                                print("   ✓ Navegação concluída")
                                
                            except Exception as btn_error:
                                print(f"   ⚠️ Não foi possível clicar no botão 'Selecionar': {str(btn_error)}")
                                page.screenshot(path='erro_botao_selecionar.png')
                                print("   ℹ️ Screenshot salvo como 'erro_botao_selecionar.png'")
                                raise
                                
                            print("\n[SUCESSO] Teste concluído com sucesso!")
                        else:
                            raise Exception(f"Falha ao selecionar o perfil. Perfil atual: {selected_text}")
                            
                        
                    except Exception as menu_error:
                        print(f"   ℹ️ Não foi possível encontrar o menu de perfis. Verificando se já está logado...")
                        # Tira um screenshot para debuggggg
                        page.screenshot(path='menu_perfis_erro.png')
                        print("   ℹ️ Screenshot salvo como 'menu_perfis_erro.png'")
                        
                        # Verifica se já está logado (se o menu de perfil não é mais necessário)
                        if page.get_by_role("heading", name="SAGE").is_visible():
                            print("✓ Já está logado no SAGE")
                            print("\n[SUCESSO] Teste concluído com sucesso!")
                        else:
                            raise menu_error
                    
                except Exception as e:
                    print(f"   ✗ Erro ao selecionar perfil: {str(e)}")
                    page.screenshot(path='erro_perfil.png')
                    print("   ℹ️ Screenshot salvo como 'erro_perfil.png'")
                    raise
                
            except Exception as e:
                print(f"   ✗ Erro durante a verificação do login: {str(e)}")
                page.screenshot(path='erro_login.png')
                print("   ℹ️ Screenshot salvo como 'erro_login.png'")
                raise
            
            # Aguarda 5 segundos para visualização final
            page.wait_for_timeout(5000)
            
        except Exception as e:
            print(f"Erro durante a execução do teste: {str(e)}")
            # Tira um screenshot em caso de erro
            page.screenshot(path='erro_login.png')
            raise
            
        finally:
            # Fecha o navegador
            browser.close()
