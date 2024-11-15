#!/bin/bash

db_name="socioclub"
db_user="socioclub"  # Define o usuário do banco de dados

# Solicita o nome da tabela
read -p "Informe o nome da tabela: " table_name

# Verifica se o nome da tabela foi fornecido
if [ -z "$table_name" ]; then
    echo "Erro: Nome da tabela não fornecido."
    exit 1
fi

read -p "Quantas inserções deseja fazer? " quantidade

if ! echo "$quantidade" | grep -qE '^[0-9]+$' || [ "$quantidade" -gt 1000 ]; then
    echo "Erro: Quantidade inválida ou acima do limite permitido (1000)."
    exit 1
fi

# Obtém as colunas e tipos
columns=($(psql -U "$db_user" -d "$db_name" -t -c "SELECT column_name FROM information_schema.columns WHERE table_name='$table_name' AND column_name != 'id';"))
types=($(psql -U "$db_user" -d "$db_name" -t -c "SELECT data_type FROM information_schema.columns WHERE table_name='$table_name' AND column_name != 'id';"))

if [ ${#columns[@]} -eq 0 ]; then
    echo "Erro: Tabela '$table_name' não encontrada ou não possui colunas além do ID."
    exit 1
fi

# Função para gerar valores realistas de acordo com o tipo de dados
generate_random_value() {
    case $1 in
        "cpf")
            printf "'%03d.%03d.%03d-%02d'" $((RANDOM % 1000)) $((RANDOM % 1000)) $((RANDOM % 1000)) $((RANDOM % 100))  # Gera um CPF fictício
            ;;
        "name")
            local names=("Ana" "Bruno" "Carlos" "Daniela" "Eduardo" "Fernanda" "Gabriel" "Helena" "Isabela" "João")
            printf "'%s'" "${names[RANDOM % ${#names[@]}]}"
            ;;
        "email")
            local username="usuario$((RANDOM % 10000))"
            printf "'%s'" "$username@gmail.com"
            ;;
        "password")
            printf "'%s'" "$(tr -dc 'A-Za-z0-9' < /dev/urandom | head -c 8)"  # Gera uma senha aleatória de 8 caracteres
            ;;
        "logo"|"background")
            printf "'https://example.com/images/%s.png'" "$(tr -dc 'A-Za-z0-9' < /dev/urandom | head -c 8)"
            ;;
        "description")
            local descriptions=("Descrição do Produto A" "Descrição do Produto B" "Produto C é excelente" "Produto D com alta qualidade" "Produto E - O melhor da categoria")
            printf "'%s'" "${descriptions[RANDOM % ${#descriptions[@]}]}"
            ;;
        "cnpj")
            printf "'%02d.%03d.%03d/%04d-%02d'" $((RANDOM % 100)) $((RANDOM % 1000)) $((RANDOM % 1000)) $((RANDOM % 10000)) $((RANDOM % 100))  # Gera um CNPJ fictício
            ;;
        "primary_color"|"secondary_color")
            printf "'#%06X'" $((RANDOM % 0xFFFFFF))  # Gera uma cor hexadecimal aleatória
            ;;
        "address")
            printf "'Rua %s, %d'" "$(tr -dc 'A-Za-z' < /dev/urandom | head -c 10)" $((RANDOM % 1000 + 1))  # Gera um endereço fictício
            ;;
        "fk_club_id"|"fk_productcategory_id"|"fk_client_id")
            echo "1"  # Insere o valor fixo '1' para essas colunas
            ;;
        "event_date"|"publish_date")
            year=$(date +%Y)
            month=$((RANDOM % 12 + 1))
            day=$((RANDOM % 28 + 1))
            printf "'%04d-%02d-%02d'" "$year" "$month" "$day"  # Data aleatória
            ;;
        "tickets_away"|"tickets_home")
            echo $((RANDOM % 500 + 1))  # Número aleatório de ingressos entre 1 e 500
            ;;
        "full_price"|"price")
            printf "%.2f" "$(echo "$((RANDOM % 1000 + 10)).$((RANDOM % 99))")"  # Preço entre 10.00 e 1009.99
            ;;
        "discount")
            echo $((RANDOM % 50))  # Desconto entre 0 e 49%
            ;;
        "priority")
            echo $((RANDOM % 5 + 1))  # Nível de prioridade entre 1 e 5
            ;;
        "text")
            local sentences=("Este é um texto de exemplo." "Texto gerado automaticamente para testes." "Conteúdo fictício para campo de texto." "Aqui está uma amostra de texto aleatório.")
            printf "'%s'" "${sentences[RANDOM % ${#sentences[@]}]}"
            ;;
        "image")
            printf "'https://example.com/images/%s.png'" "$(tr -dc 'A-Za-z0-9' < /dev/urandom | head -c 8)"
            ;;
        "author")
            local authors=("João Silva" "Maria Souza" "Carlos Alberto" "Fernanda Lima" "Roberto Costa")
            printf "'%s'" "${authors[RANDOM % ${#authors[@]}]}"
            ;;
        "title")
            local titles=("Título de Exemplo" "Introdução ao SQL" "Como Programar em Bash" "Aprendendo Python" "Guia Completo de PostgreSQL")
            printf "'%s'" "${titles[RANDOM % ${#titles[@]}]}"
            ;;
        "qr_code")
            printf "'QR-%04d'" $((RANDOM % 10000))  # Gera um QR code fictício
            ;;
        "fk_event_id")
            echo $((RANDOM % 5 + 1))  # Nível de prioridade entre 1 e 5
            ;;
        *)
            echo "NULL"
            ;;
    esac
}

# Loop para fazer as inserções
for ((i = 1; i <= quantidade; i++)); do
    values=""

    for ((j = 0; j < ${#columns[@]}; j++)); do
        random_value=$(generate_random_value "${columns[$j]}")

        values+="$random_value"

        if [ $j -lt $((${#columns[@]} - 1)) ]; then
            values+=", "
        fi
    done

    column_names=$(IFS=, ; echo "${columns[*]}")

    sql="INSERT INTO $table_name ($column_names) VALUES ($values);"

    echo "Comando SQL: $sql"

    psql -U "$db_user" -d "$db_name" -c "$sql"

    if [ $? -eq 0 ]; then
        echo "Linha $i inserida com valores realistas."
    else
        echo "Erro ao inserir linha $i."
    fi
done
