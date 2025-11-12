"""
Landing Page Agent 메인 실행 파일이다.
"""
import asyncio
import argparse
import sys
import os
from pathlib import Path
import logging
from typing import Optional
import json

# UTF-8 인코딩 강제 설정
if sys.platform == 'darwin' or sys.platform == 'linux':
    import locale
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except:
        pass

# 표준 입출력 인코딩 설정
sys.stdin.reconfigure(encoding='utf-8', errors='replace')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from config import config
from agent import ClaudeClient, LandingPageGenerator
from models.validation import AgentRequest

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Rich Console 설정
console = Console()


def parse_arguments() -> argparse.Namespace:
    """
    커맨드 라인 인자를 파싱한다.
    
    Returns:
        argparse.Namespace: 파싱된 인자
    """
    parser = argparse.ArgumentParser(
        description="Claude Sonnet 4.5를 사용한 랜딩 페이지 생성 Agent이다"
    )
    
    parser.add_argument(
        "--skills-dir",
        type=str,
        help="Skills 디렉토리 경로를 지정한다",
        default=None
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        help="출력 디렉토리 경로를 지정한다",
        default=None
    )
    
    parser.add_argument(
        "--max-retries",
        type=int,
        help="최대 재시도 횟수를 지정한다",
        default=3
    )
    
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="비대화형 모드로 실행한다"
    )
    
    parser.add_argument(
        "--config-file",
        type=str,
        help="설정 파일 경로를 지정한다 (JSON)",
        default=None
    )
    
    return parser.parse_args()


def load_config_file(config_file: str) -> Optional[AgentRequest]:
    """
    설정 파일에서 요청 정보를 로드한다.
    
    Args:
        config_file: 설정 파일 경로
        
    Returns:
        Optional[AgentRequest]: 요청 정보 또는 None
    """
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return AgentRequest(**data)
    except Exception as e:
        console.print(f"[red]설정 파일 로드 실패: {str(e)}[/red]")
        return None


def display_welcome() -> None:
    """
    환영 메시지를 표시한다.
    """
    welcome_text = """
[bold cyan]Landing Page Agent[/bold cyan]

Claude Sonnet 4.5를 활용한 고품질 랜딩 페이지 자동 생성 도구이다.

[yellow]주요 기능:[/yellow]
• 11가지 필수 요소를 포함하는 완벽한 랜딩 페이지 생성
• Next.js 14+ App Router + TypeScript + ShadCN UI 사용
• 실시간 대화형 생성 프로세스
• 자동 에러 복구 및 재시도
• 프로덕션 레벨 코드 품질
"""
    
    console.print(Panel(welcome_text, border_style="cyan"))


def get_user_input_interactive() -> AgentRequest:
    """
    대화형 방식으로 사용자 입력을 받는다.
    
    Returns:
        AgentRequest: 사용자 요청
    """
    import sys
    
    console.print("\n[bold]프로젝트 정보를 입력한다:[/bold]\n")
    
    # 표준 input()을 사용하여 인코딩 문제를 우회한다
    try:
        print("프로젝트명 [my-landing-page]: ", end="", flush=True)
        project_name = input().strip() or "my-landing-page"
        
        print("제품/서비스명: ", end="", flush=True)
        product_name = input().strip()
        
        print("제품/서비스 설명: ", end="", flush=True)
        description = input().strip()
        
        print("타겟 고객 [일반 사용자]: ", end="", flush=True)
        target_audience = input().strip() or "일반 사용자"
        
        print("브랜드 색상 [blue]: ", end="", flush=True)
        brand_color = input().strip() or "blue"
        
        console.print("\n[bold]주요 기능을 입력한다 (빈 입력으로 완료):[/bold]")
        key_features = []
        index = 1
        
        while True:
            print(f"기능 {index}: ", end="", flush=True)
            feature = input().strip()
            if not feature:
                break
            key_features.append(feature)
            index += 1
        
    except UnicodeDecodeError as e:
        console.print(f"[red]입력 인코딩 에러가 발생했다: {str(e)}[/red]")
        console.print("[yellow]환경 변수를 설정한다: export LC_ALL=en_US.UTF-8[/yellow]")
        raise
    
    return AgentRequest(
        project_name=project_name,
        product_name=product_name,
        description=description,
        target_audience=target_audience,
        key_features=key_features,
        brand_color=brand_color
    )


def display_request_summary(request: AgentRequest) -> None:
    """
    요청 정보 요약을 표시한다.
    
    Args:
        request: 요청 정보
    """
    table = Table(title="프로젝트 정보", show_header=False, border_style="cyan")
    table.add_column("항목", style="cyan", width=20)
    table.add_column("내용", style="white")
    
    table.add_row("프로젝트명", request.project_name)
    table.add_row("제품/서비스명", request.product_name)
    table.add_row("설명", request.description)
    table.add_row("타겟 고객", request.target_audience)
    table.add_row("브랜드 색상", request.brand_color)
    
    if request.key_features:
        features_text = "\n".join(f"• {f}" for f in request.key_features)
        table.add_row("주요 기능", features_text)
    
    console.print("\n")
    console.print(table)
    console.print("\n")


async def initialize_client(skills_dir: Path) -> ClaudeClient:
    """
    Claude 클라이언트를 초기화한다.
    
    Args:
        skills_dir: Skills 디렉토리 경로
        
    Returns:
        ClaudeClient: 초기화된 클라이언트
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Claude 클라이언트를 초기화한다...", total=None)
        
        client = ClaudeClient()
        await client.load_skill(skills_dir)
        
        progress.update(task, completed=True)
    
    console.print("[green]✓ 클라이언트 초기화 완료[/green]\n")
    return client


async def generate_landing_page(
    generator: LandingPageGenerator,
    interactive: bool = True
) -> None:
    """
    랜딩 페이지를 생성한다.
    
    Args:
        generator: 랜딩 페이지 생성기
        interactive: 대화형 모드 여부
    """
    console.print("[bold cyan]랜딩 페이지 생성을 시작한다...[/bold cyan]\n")
    
    try:
        validation = await generator.generate_all_components(interactive=interactive)
        
        # README 생성
        await generator.generate_readme()
        
        # 리포트 저장
        report = generator.export_report()
        report_path = generator.output_dir / "generation_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        console.print(f"\n[green]✓ 생성 리포트 저장: {report_path}[/green]")
        
    except Exception as e:
        console.print(f"\n[red]✗ 생성 중 에러 발생: {str(e)}[/red]")
        logger.error(f"생성 에러: {str(e)}", exc_info=True)
        raise


def display_final_summary(output_dir: Path, generator: LandingPageGenerator) -> None:
    """
    최종 요약 정보를 표시한다.
    
    Args:
        output_dir: 출력 디렉토리
        generator: 랜딩 페이지 생성기
    """
    validation_result = generator.validation.validate_all_elements()
    
    summary_panel = f"""
[bold]생성 완료![/bold]

[cyan]출력 디렉토리:[/cyan] {output_dir}
[cyan]생성된 컴포넌트 수:[/cyan] {len(generator.validation.components)}
[cyan]검증 결과:[/cyan] {"✓ 통과" if validation_result.is_valid else "✗ 실패"}

[yellow]다음 단계:[/yellow]
1. cd {output_dir}
2. npm install
3. npm run dev
4. 브라우저에서 http://localhost:3000 열기
"""
    
    if validation_result.missing_elements:
        summary_panel += f"\n[red]누락된 요소:[/red] {validation_result.missing_elements}"
    
    if validation_result.warnings:
        summary_panel += "\n[yellow]경고:[/yellow]"
        for warning in validation_result.warnings:
            summary_panel += f"\n  • {warning}"
    
    console.print(Panel(summary_panel, border_style="green", title="✓ 완료"))


async def main() -> int:
    """
    메인 실행 함수이다.
    
    Returns:
        int: 종료 코드
    """
    try:
        # 인자 파싱
        args = parse_arguments()
        
        # 설정 적용
        if args.skills_dir:
            config.set_skills_dir(args.skills_dir)
        
        if args.output_dir:
            config.set_output_dir(args.output_dir)
        else:
            # 기본 출력 디렉토리 생성
            config.set_output_dir(str(config.BASE_DIR / "output"))
        
        config.set_max_retries(args.max_retries)
        
        # 설정 검증
        try:
            config.validate()
        except Exception as e:
            console.print(f"[red]설정 검증 실패: {str(e)}[/red]")
            return 1
        
        # 환영 메시지
        if not args.non_interactive:
            display_welcome()
        
        # 요청 정보 수집
        if args.config_file:
            request = load_config_file(args.config_file)
            if not request:
                return 1
        elif args.non_interactive:
            console.print("[red]비대화형 모드에서는 --config-file 옵션이 필요하다[/red]")
            return 1
        else:
            request = get_user_input_interactive()
        
        # 요청 정보 표시
        display_request_summary(request)
        
        # 확인
        if not args.non_interactive:
            if not Confirm.ask("위 정보로 생성을 시작할까?"):
                console.print("[yellow]생성이 취소되었다[/yellow]")
                return 0
        
        # 출력 디렉토리 생성
        output_dir = Path(config.OUTPUT_DIR)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 클라이언트 초기화
        client = await initialize_client(Path(config.SKILLS_DIR))
        
        # 생성기 초기화
        generator = LandingPageGenerator(client, output_dir)
        generator.set_request(request)
        
        # 랜딩 페이지 생성
        await generate_landing_page(generator, interactive=not args.non_interactive)
        
        # 최종 요약
        display_final_summary(output_dir, generator)
        
        return 0
        
    except KeyboardInterrupt:
        console.print("\n[yellow]사용자가 중단했다[/yellow]")
        return 130
    except Exception as e:
        console.print(f"\n[red]예상치 못한 에러 발생: {str(e)}[/red]")
        logger.error(f"메인 에러: {str(e)}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))