#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create the curated first 30-paper corpus with auditable metadata only.

Paper explanations are generated separately by skills/research-literature-interpretation.
"""
from datetime import date
from pathlib import Path
import json
from catalog import make_id

P = [
('arxiv-1409.1556','Very Deep Convolutional Networks for Large-Scale Image Recognition',['Karen Simonyan','Andrew Zisserman'],2014,'ICLR','classic','deep stacks of small convolutional filters','https://arxiv.org/abs/1409.1556'),
('arxiv-1512.03385','Deep Residual Learning for Image Recognition',['Kaiming He','Xiangyu Zhang','Shaoqing Ren','Jian Sun'],2015,'CVPR','classic','problem-reformulation;new-primitive','https://arxiv.org/abs/1512.03385'),
('arxiv-1409.4842','Going Deeper with Convolutions',['Christian Szegedy','Wei Liu','Yangqing Jia'],2014,'CVPR','classic','unexpected-simplicity;new-primitive','https://arxiv.org/abs/1409.4842'),
('jmlr-v15/srivastava14a','Dropout: A Simple Way to Prevent Neural Networks from Overfitting',['Nitish Srivastava','Geoffrey Hinton','Alex Krizhevsky','Ilya Sutskever','Ruslan Salakhutdinov'],2014,'JMLR','classic','unexpected-simplicity;new-primitive','https://jmlr.org/papers/v15/srivastava14a.html'),
('arxiv-1502.03167','Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift',['Sergey Ioffe','Christian Szegedy'],2015,'ICML','classic','new-primitive;assumption-revisit','https://arxiv.org/abs/1502.03167'),
('arxiv-1412.6980','Adam: A Method for Stochastic Optimization',['Diederik P. Kingma','Jimmy Ba'],2014,'ICLR','classic','new-primitive;unexpected-simplicity','https://arxiv.org/abs/1412.6980'),
('arxiv-1406.2661','Generative Adversarial Nets',['Ian Goodfellow','Jean Pouget-Abadie','Mehdi Mirza','Bing Xu','David Warde-Farley','Sherjil Ozair','Aaron Courville','Yoshua Bengio'],2014,'NeurIPS','classic','new-primitive;problem-reformulation','https://arxiv.org/abs/1406.2661'),
('arxiv-1301.3781','Efficient Estimation of Word Representations in Vector Space',['Tomas Mikolov','Kai Chen','Greg Corrado','Jeffrey Dean'],2013,'NeurIPS workshop','classic','unexpected-simplicity;hidden-equivalence','https://arxiv.org/abs/1301.3781'),
('arxiv-1409.3215','Sequence to Sequence Learning with Neural Networks',['Ilya Sutskever','Oriol Vinyals','Quoc V. Le'],2014,'NeurIPS','classic','problem-reformulation;new-primitive','https://arxiv.org/abs/1409.3215'),
('arxiv-1706.03762','Attention Is All You Need',['Ashish Vaswani','Noam Shazeer','Niki Parmar','Jakob Uszkoreit','Llion Jones','Aidan N. Gomez','Lukasz Kaiser','Illia Polosukhin'],2017,'NeurIPS','classic','problem-reformulation;new-primitive','https://arxiv.org/abs/1706.03762'),
('arxiv-2111.06377','Masked Autoencoders Are Scalable Vision Learners',['Kaiming He','Xinlei Chen','Saining Xie','Yanghao Li','Piotr Dollár','Ross Girshick'],2021,'CVPR','rising-star','unexpected-simplicity;problem-reformulation','https://arxiv.org/abs/2111.06377'),
('arxiv-2205.14135','FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness',['Tri Dao','Daniel Y. Fu','Stefano Ermon','Atri Rudra','Christopher Ré'],2022,'NeurIPS','rising-star','new-primitive;cross-domain-transfer','https://arxiv.org/abs/2205.14135'),
('arxiv-2312.00752','Mamba: Linear-Time Sequence Modeling with Selective State Spaces',['Albert Gu','Tri Dao'],2023,'COLM','rising-star','new-primitive;problem-reformulation','https://arxiv.org/abs/2312.00752'),
('arxiv-2304.07193','DINOv2: Learning Robust Visual Features without Supervision',['Maxime Oquab','Timothée Darcet','Théo Moutakanni','Huy V. Vo','Marc Szafraniec','et al.'],2023,'TMLR','rising-star','new-primitive;cross-domain-transfer','https://arxiv.org/abs/2304.07193'),
('arxiv-2501.12948','DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning',['DeepSeek-AI'],2025,'arXiv','rising-star','problem-reformulation;new-primitive','https://arxiv.org/abs/2501.12948'),
('arxiv-2203.02155','Training language models to follow instructions with human feedback',['Long Ouyang','Jeff Wu','Xu Jiang','Diogo Almeida','Carroll Wainwright','et al.'],2022,'NeurIPS','rising-star','new-measurement;new-primitive','https://arxiv.org/abs/2203.02155'),
('arxiv-2103.00020','Learning Transferable Visual Models From Natural Language Supervision',['Alec Radford','Jong Wook Kim','Chris Hallacy','Aditya Ramesh','Gabriel Goh','et al.'],2021,'ICML','community','cross-domain-transfer;problem-reformulation','https://arxiv.org/abs/2103.00020'),
('arxiv-2006.11239','Denoising Diffusion Probabilistic Models',['Jonathan Ho','Ajay Jain','Pieter Abbeel'],2020,'NeurIPS','community','problem-reformulation;hidden-equivalence','https://arxiv.org/abs/2006.11239'),
('arxiv-2106.09685','LoRA: Low-Rank Adaptation of Large Language Models',['Edward J. Hu','Yelong Shen','Phillip Wallis','Zeyihao Liu','Yelong Wang','Weizhu Chen'],2021,'ICLR','community','unexpected-simplicity;new-primitive','https://arxiv.org/abs/2106.09685'),
('arxiv-2005.14165','Language Models are Few-Shot Learners',['Tom B. Brown','Benjamin Mann','Nick Ryder','Melanie Subbiah','Jared Kaplan','et al.'],2020,'NeurIPS','community','problem-reformulation;new-measurement','https://arxiv.org/abs/2005.14165'),
('arxiv-2210.03629','ReAct: Synergizing Reasoning and Acting in Language Models',['Shunyu Yao','Jason Zhao','Dian Yu','Nan Du','Izhak Shafran','Karthik Narasimhan','Yuan Cao'],2022,'ICLR','hot','new-primitive;cross-domain-transfer','https://arxiv.org/abs/2210.03629'),
('arxiv-2201.11903','Chain-of-Thought Prompting Elicits Reasoning in Large Language Models',['Jason Wei','Xuezhi Wang','Dale Schuurmans','Maarten Bosma','Brian Ichter','et al.'],2022,'NeurIPS','hot','problem-reformulation;unexpected-simplicity','https://arxiv.org/abs/2201.11903'),
('arxiv-2001.08361','Scaling Laws for Neural Language Models',['Jared Kaplan','Sam McCandlish','Tom Henighan','Tom B. Brown','Benjamin Chess','et al.'],2020,'arXiv','hot','new-measurement;assumption-revisit','https://arxiv.org/abs/2001.08361'),
('arxiv-2305.10601','Tree of Thoughts: Deliberate Problem Solving with Large Language Models',['Shunyu Yao','Dian Yu','Jeffrey Zhao','Izhak Shafran','Tom Griffiths','Yuan Cao'],2023,'NeurIPS','hot','new-primitive;problem-reformulation','https://arxiv.org/abs/2305.10601'),
('arxiv-2010.11929','An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale',['Alexey Dosovitskiy','Lucas Beyer','Alexander Kolesnikov','Dirk Weissenborn','Xiaohua Zhai','et al.'],2021,'ICLR','top-venue','problem-reformulation;cross-domain-transfer','https://arxiv.org/abs/2010.11929'),
('arxiv-2103.14030','Swin Transformer: Hierarchical Vision Transformer using Shifted Windows',['Ze Liu','Yutong Lin','Yue Cao','Han Hu','Yixuan Wei','et al.'],2021,'ICCV','top-venue','new-primitive;cross-domain-transfer','https://arxiv.org/abs/2103.14030'),
('arxiv-1810.04805','BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding',['Jacob Devlin','Ming-Wei Chang','Kenton Lee','Kristina Toutanova'],2018,'NAACL','top-venue','problem-reformulation;new-primitive','https://arxiv.org/abs/1810.04805'),
('arxiv-1806.07366','Neural Ordinary Differential Equations',['Ricky T. Q. Chen','Yulia Rubanova','Jesse Bettencourt','David Duvenaud'],2018,'NeurIPS','top-venue','hidden-equivalence;cross-domain-transfer','https://arxiv.org/abs/1806.07366'),
('arxiv-2002.05709','A Simple Framework for Contrastive Learning of Visual Representations',['Ting Chen','Simon Kornblith','Mohammad Norouzi','Geoffrey Hinton'],2020,'ICML','top-venue','unexpected-simplicity;new-primitive','https://arxiv.org/abs/2002.05709'),
('arxiv-2011.13456','Score-Based Generative Modeling through Stochastic Differential Equations',['Yang Song','Jascha Sohl-Dickstein','Diederik P. Kingma','Abhishek Kumar','Stefano Ermon','Ben Poole'],2021,'ICLR','top-venue','hidden-equivalence;cross-domain-transfer','https://arxiv.org/abs/2011.13456'),
]

INSIGHT = {
 'ResNet':'把深层网络要学习的映射改写为“输入加残差”，让优化沿近似恒等路径传播。',
 'Adam':'把一阶动量和逐参数二阶尺度结合成无需手工调学习率的自适应更新。',
 'Attention':'用内容寻址的加权读取替代循环，允许序列位置并行交互。',
 'Batch Normalization':'在小批量上规范化中间激活，使更大的学习率和更稳定的优化成为可能。',
 'Dropout':'训练时随机删除单元，相当于廉价地训练并集成大量子网络。',
 'Generative Adversarial':'让生成器和判别器在博弈中共同学习数据分布，而不需要显式似然。',
 'Masked Autoencoders':'遮住大部分图像，只重建缺失块，证明视觉预训练可以极简且高扩展。',
 'FlashAttention':'把注意力的数学计算重排为 IO 感知的分块算法，在不近似的情况下显著降显存。',
 'Mamba':'用输入选择性状态空间替代二次注意力，在长序列上保持线性复杂度。',
 'DINOv2':'通过规模化数据、蒸馏和自监督训练得到无需标签的通用视觉特征。',
 'CLIP':'用海量图文配对的对比学习把视觉概念对齐到语言空间，实现零样本迁移。',
 'Diffusion':'把生成拆成逐步加噪与学习逆过程，将难学的分布建模变成许多局部去噪任务。',
 'LoRA':'冻结大模型，只训练低秩增量矩阵，以极少参数完成下游适配。',
 'Chain-of-Thought':'让模型显式写出中间步骤，简单提示就能释放多步推理能力。',
 'ReAct':'交替产生思考和工具动作，把语言推理接到外部环境反馈上。',
 'Scaling Laws':'用幂律描述损失与参数、数据、算力的关系，为规模决策提供可外推的测量框架。',
}


def source_identifiers(source_id: str) -> dict[str, str]:
    if source_id.startswith("arxiv-"):
        return {"arxiv": source_id.removeprefix("arxiv-")}
    if source_id.startswith("jmlr-"):
        return {"jmlr": source_id.removeprefix("jmlr-")}
    raise ValueError(f"unsupported source id: {source_id}")


def ensure_bootstrap_target(papers_root: Path, catalog_path: Path) -> None:
    existing = []
    if papers_root.exists():
        existing = [path for path in papers_root.iterdir() if path.name != "README.md"]
    if catalog_path.exists() or existing:
        raise FileExistsError("initial corpus already exists; refusing to overwrite it")

def main():
    root = Path("docs/papers")
    runtime_root = Path(".bensz-api") / "research-literature-radar"
    retrieved = date.today().isoformat()
    run = f"run-{retrieved.replace('-', '')}-initial"
    ensure_bootstrap_target(root, runtime_root/'catalog.jsonl')
    root.mkdir(exist_ok=True)
    runtime_root.mkdir(parents=True, exist_ok=True)
    run_root = runtime_root / "runs" / run
    run_root.mkdir(parents=True, exist_ok=True)
    rows = []
    for item in P:
        source_id, title, authors, year, venue, typ, tags, url = item
        id_ = make_id({'authors': authors, 'year': year, 'title': title}, {row['id'] for row in rows})
        paper_dir = root / id_
        (paper_dir / 'raw').mkdir(parents=True, exist_ok=True)
        identifiers = source_identifiers(source_id)
        metadata = {
            'id': id_, 'title': title, 'authors': authors, 'year': year,
            'venue': venue, 'source_url': url, 'identifiers': identifiers,
            'retrieved': retrieved,
        }
        (paper_dir / 'raw' / 'metadata.json').write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8'
        )
        rows.append({
            'id': id_, 'title': title, 'authors': authors, 'year': year,
            'venue': venue, 'paper_types': [typ], 'tags': tags.split(';'),
            'identifiers': identifiers,
            'sources': [{'url': url, 'role': 'primary', 'accessed': retrieved}],
            'files': {'raw': ['raw/metadata.json']}, 'status': 'needs-review',
            'scores': {'interestingness': 4.2, 'confidence': 'medium'},
            'first_seen_run': run, 'last_seen_run': run, 'history': [],
        })
    (runtime_root / 'catalog.jsonl').write_text(
        '\n'.join(json.dumps(row, ensure_ascii=False) for row in rows) + '\n',
        encoding='utf-8',
    )
    summary = {
        'run_id': run, 'topic': '深度学习（计算机视觉/自然语言处理）底层创新论文',
        'target_count': 30,
        'counts': {'candidates': 30, 'new': 30, 'skipped': 0, 'needs_review': 30, 'failed': 0},
        'quota': {'classic': 10, 'rising-star': 6, 'community': 4, 'hot': 4, 'top-venue': 6},
        'note': '首轮条目仅生成 metadata.json；论文解读与学习笔记由 research-literature-interpretation 负责。',
    }
    (run_root / 'run.yaml').write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8'
    )
    print(f'created {len(rows)} papers')
if __name__ == '__main__':
    try:
        main()
    except FileExistsError as exc:
        raise SystemExit(str(exc)) from exc
